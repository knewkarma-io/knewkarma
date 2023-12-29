' Necessary imports
Imports System.Net.Http
Imports Newtonsoft.Json.Linq
Imports System.Runtime.InteropServices
Imports System.Reflection

Public Class ApiHandler

    Private BASE_REDDIT_ENDPOINT As String = "https://www.reddit.com"
    Private USER_DATA_ENDPOINT As String = $"{BASE_REDDIT_ENDPOINT}/u"
    Private USERS_DATA_ENDPOINT As String = $"{BASE_REDDIT_ENDPOINT}/users"
    Private COMMUNITY_DATA_ENDPOINT As String = $"{BASE_REDDIT_ENDPOINT}/r"
    Private COMMUNITIES_DATA_ENDPOINT As String = $"{BASE_REDDIT_ENDPOINT}/subreddits"
    Private GITHUB_RELEASE_ENDPOINT As String = "https://api.github.com/repos/bellingcat/knewkarma/releases/latest"

    Private ReadOnly appVersion As String = $"{My.Application.Info.Version.Major}.{My.Application.Info.Version.Minor}"
    Private ReadOnly dotNetVersion As String = RuntimeInformation.FrameworkDescription


    Public Async Function AsyncGetData(endpoint As String) As Task(Of JToken)
        Try
            Using httpClient As New HttpClient()
                httpClient.DefaultRequestHeaders.Add(
                "User-Agent",
                $"Knew-Karma/{appVersion} (.NET {dotNetVersion}; +https:rly0nheart.github.io)"
            )

                Dim response As HttpResponseMessage = Await httpClient.GetAsync(endpoint)

                If response.IsSuccessStatusCode Then
                    Dim json As String = Await response.Content.ReadAsStringAsync()
                    Return JToken.Parse(json)
                Else
                    MessageBox.Show($"Error: {response.StatusCode} - {response.ReasonPhrase}", "API Request Error", MessageBoxButtons.OK, MessageBoxIcon.Error)
                    Return Nothing
                End If
            End Using
        Catch ex As HttpRequestException
            MessageBox.Show($"HTTP Request Error: {ex.Message}", "Network Error", MessageBoxButtons.OK, MessageBoxIcon.Error)
            Return Nothing
        Catch ex As Exception
            MessageBox.Show($"An error occurred: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error)
            Return Nothing
        End Try
    End Function

    Private Async Function FetchAndPaginateAsync(endpoint As String, limit As Integer) As Task(Of JArray)
        Dim allItems As New JArray()
        Dim lastItemId As String = String.Empty
        Dim paginate As Boolean = limit > 100

        While allItems.Count < limit
            Dim paginationEndpoint As String = If(paginate And Not String.IsNullOrEmpty(lastItemId), $"{endpoint}&after={lastItemId}", endpoint)
            Dim responseData As JObject = Await AsyncGetData(paginationEndpoint)
            Dim dataItems As JArray = ProcessApiResponse(responseData("data")("children"), "data")

            If dataItems.Count = 0 Then
                Exit While
            End If

            allItems.Merge(dataItems)
            lastItemId = dataItems.Last("data")("id").ToString()

            If allItems.Count >= limit Then
                Exit While
            End If
        End While

        Return allItems
    End Function


    Private Shared Function ProcessApiResponse(data As JToken, validKey As String) As JToken
        If data Is Nothing Then
            Return New JObject()
        End If

        If data.Type = JTokenType.Object Then
            Dim dataObj As JObject = CType(data, JObject)
            If Not String.IsNullOrEmpty(validKey) AndAlso dataObj.ContainsKey(validKey) Then
                Return dataObj
            Else
                MessageBox.Show($"The expected key '{validKey}' was not found in the response.", "API Response Error", MessageBoxButtons.OK, MessageBoxIcon.Error)
                Return New JObject()
            End If
        ElseIf data.Type = JTokenType.Array Then
            Dim dataArray As JArray = CType(data, JArray)
            If dataArray.Count > 0 Then
                Return dataArray
            Else
                MessageBox.Show("The response array is empty.", "API Response Error", MessageBoxButtons.OK, MessageBoxIcon.Error)
                Return New JArray()
            End If
        Else
            MessageBox.Show($"Unexpected data type in response: {data.Type}", "API Response Error", MessageBoxButtons.OK, MessageBoxIcon.Error)
            Return New JObject()
        End If
    End Function


    Public Async Function AsyncGetProfile(type As String, from As String) As Task(Of JObject)
        Dim endpointMap As New Dictionary(Of String, String) From {
        {"user", $"{USER_DATA_ENDPOINT}/{from}/about.json"},
        {"community", $"{COMMUNITY_DATA_ENDPOINT}/{from}/about.json"}
    }

        If endpointMap.ContainsKey(type) Then
            Dim endpoint As String = endpointMap(type)
            Dim response As JToken = Await AsyncGetData(endpoint)
            Dim processedResponse As JObject = CType(ProcessApiResponse(response, "data"), JObject)
            Return processedResponse("data")
        Else
            ' Log an error for invalid profile type
            ' LogError($"Invalid profile type: {profileType}")
            Return New JObject()
        End If
    End Function

    ' Async function to get posts with pagination
    Public Async Function AsyncGetPosts(
        ByVal limit As Integer,
        ByVal type As String,
        Optional ByVal from As String = Nothing,
        Optional ByVal sort As String = "all",
        Optional ByVal timeframe As String = "all"
    ) As Task(Of JArray)

        Dim postsTypeMap As New Dictionary(Of String, String) From {
        {"new", $"{BASE_REDDIT_ENDPOINT}/new.json"},
        {"front_page", $"{BASE_REDDIT_ENDPOINT}/.json"},
        {"listing", $"{COMMUNITY_DATA_ENDPOINT}/{from}.json"},
        {"community", $"{COMMUNITY_DATA_ENDPOINT}/{from}.json"},
        {"user_posts", $"{USER_DATA_ENDPOINT}/{from}/submitted.json"},
        {"user_overview", $"{USER_DATA_ENDPOINT}/{from}/overview.json"},
        {"user_comments", $"{USER_DATA_ENDPOINT}/{from}/comments.json"}
    }
        If Not postsTypeMap.ContainsKey(type) Then
            Throw New ArgumentException($"Invalid post type: {type}")
        End If

        Dim postsEndpoint As String = postsTypeMap(type)

        If type = "new" Then
            postsEndpoint &= $"?limit={limit}&sort={sort}"
        Else
            postsEndpoint &= $"?limit={limit}&sort={sort}&t={timeframe}"
        End If



        Return Await FetchAndPaginateAsync(endpoint:=postsEndpoint, limit:=limit)
    End Function


    ' Async function to perform a search
    Public Async Function AsyncSearch(searchType As String, query As String, limit As Integer) As Task(Of JArray)
        Dim sourceMap As New Dictionary(Of String, String) From {
        {"users", $"{USERS_DATA_ENDPOINT}/search.json?q={query}"},
        {"communities", $"{COMMUNITIES_DATA_ENDPOINT}/search.json?q={query}"},
        {"posts", $"{BASE_REDDIT_ENDPOINT}/search.json?q={query}"}
    }

        If Not sourceMap.ContainsKey(searchType) Then
            Throw New ArgumentException($"Invalid search type: {searchType}")
        End If

        Dim searchEndpoint As String = sourceMap(searchType)
        searchEndpoint &= $"&limit={limit}"

        Return Await FetchAndPaginateAsync(endpoint:=searchEndpoint, limit:=limit)
    End Function


    ' Async function to get communities
    Public Async Function AsyncGetCommunities(communityType As String, limit As Integer) As Task(Of JArray)
        Dim sourceMap As New Dictionary(Of String, String) From {
         {"all", $"{COMMUNITIES_DATA_ENDPOINT}.json"},
         {"default", $"{COMMUNITIES_DATA_ENDPOINT}/default.json"},
         {"new", $"{COMMUNITIES_DATA_ENDPOINT}/new.json"},
         {"popular", $"{COMMUNITIES_DATA_ENDPOINT}/popular.json"}
     }

        If Not sourceMap.ContainsKey(communityType) Then
            Throw New ArgumentException($"Invalid community type: {communityType}")
        End If

        Dim communityEndpoint As String = sourceMap(communityType)
        communityEndpoint &= $"?limit={limit}"

        Dim responseData As JObject = Await AsyncGetData(communityEndpoint)
        Dim communities As JArray = ProcessApiResponse(responseData("data")("children"), "data")

        Return communities
    End Function
End Class
