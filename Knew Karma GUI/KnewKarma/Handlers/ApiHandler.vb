' Necessary imports
Imports System.Net.Http
Imports Newtonsoft.Json.Linq
Imports System.Runtime.InteropServices
Imports System.Reflection
Imports Microsoft.VisualBasic.Logging
Imports System.Globalization

''' <summary>
''' Handles API requests and data processing for Reddit and GitHub.
''' </summary>
Public Class ApiHandler

    Private ReadOnly BASE_REDDIT_ENDPOINT As String = "https://www.reddit.com"
    Private ReadOnly USER_DATA_ENDPOINT As String = $"{BASE_REDDIT_ENDPOINT}/u"
    Private ReadOnly USERS_DATA_ENDPOINT As String = $"{BASE_REDDIT_ENDPOINT}/users"
    Private ReadOnly COMMUNITY_DATA_ENDPOINT As String = $"{BASE_REDDIT_ENDPOINT}/r"
    Private ReadOnly COMMUNITIES_DATA_ENDPOINT As String = $"{BASE_REDDIT_ENDPOINT}/subreddits"
    Private ReadOnly GITHUB_RELEASE_ENDPOINT As String = "https://api.github.com/repos/bellingcat/knewkarma/releases/latest"

    Private ReadOnly appVersion As String = $"{My.Application.Info.Version.Major}.{My.Application.Info.Version.Minor}"
    Private ReadOnly dotNetVersion As String = RuntimeInformation.FrameworkDescription


    ''' <summary>
    ''' Asynchronously fetches data from a specified API endpoint.
    ''' </summary>
    ''' <param name="endpoint">The API endpoint URL.</param>
    ''' <returns>JToken containing the API response, or Nothing in case of failure.</returns>
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


    ''' <summary>
    ''' Asynchronously fetches data from an API endpoint and handles pagination.
    ''' </summary>
    ''' <param name="endpoint">The API endpoint URL.</param>
    ''' <param name="limit">Maximum number of items to fetch.</param>
    ''' <returns>JArray containing paginated response data.</returns>
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


    ''' <summary>
    ''' Processes the API response, ensuring valid data is returned.
    ''' </summary>
    ''' <param name="data">The JToken response from the API.</param>
    ''' <param name="validKey">A key to validate in the response object.</param>
    ''' <returns>Processed JToken with valid data, or a default JToken in case of invalid data.</returns>
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


    ''' <summary>
    ''' Asynchronously fetches the program's update information from GitHub and compares it with the current version.
    ''' Assumes version format: major.minor.patch.prefix
    ''' </summary>
    ''' <returns>Task representing the asynchronous operation.</returns>
    Public Async Function AsyncGetUpdates() As Task
        Dim response As JObject = Await AsyncGetData(endpoint:="https://api.github.com/repos/bellingcat/knewkarma/releases/latest")
        If response IsNot Nothing AndAlso response.ContainsKey("tag_name") Then
            Dim remoteVersion As String = response("tag_name").ToString()

            ' Splitting the version strings into components
            Dim remoteParts As List(Of String) = remoteVersion.Split(".").ToList()

            Dim updateMessage As String = "{0} update available: {1}"
            Dim isUpdateAvailable As Boolean = False

            ' Check for differences in version parts
            If remoteParts(0) <> My.Application.Info.Version.Major.ToString(CultureInfo.InvariantCulture) Then
                updateMessage = String.Format(CultureInfo.InvariantCulture, updateMessage, "MAJOR", remoteVersion)
                isUpdateAvailable = True
            ElseIf remoteParts(1) <> My.Application.Info.Version.Minor.ToString(CultureInfo.InvariantCulture) Then
                updateMessage = String.Format(CultureInfo.InvariantCulture, updateMessage, "MINOR", remoteVersion)
                isUpdateAvailable = True
            ElseIf remoteParts.Count > 2 AndAlso remoteParts(2) <> My.Application.Info.Version.Build.ToString(CultureInfo.InvariantCulture) Then
                updateMessage = String.Format(CultureInfo.InvariantCulture, updateMessage, "PATCH", remoteVersion)
                isUpdateAvailable = True
            End If

            If isUpdateAvailable Then
                AboutWindow.VersionStatus.Text = updateMessage
                AboutWindow.ButtonGetUpdates.Enabled = True
            End If
        End If
    End Function


    ''' <summary>
    ''' Asynchronously retrieves a user or community profile from Reddit.
    ''' </summary>
    ''' <param name="type">The type of profile to fetch (e.g., 'user', 'community').</param>
    ''' <param name="from">Identifier for the user or community.</param>
    ''' <returns>Task representing the asynchronous operation, returning a JObject with profile data.</returns>
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
            Return New JObject()
        End If
    End Function


    ''' <summary>
    ''' Asynchronously retrieves a collection of posts from Reddit based on specified criteria.
    ''' </summary>
    ''' <param name="limit">The maximum number of posts to retrieve.</param>
    ''' <param name="type">The type of posts to retrieve, such as 'new', 'front_page', 'listing', 'community', 'user_posts', etc.</param>
    ''' <param name="from">An optional parameter specifying the source of the posts (e.g., specific user or community).</param>
    ''' <param name="sort">An optional parameter to define the sorting method of the posts (e.g., 'hot', 'new', 'top'). Default is 'all'.</param>
    ''' <param name="timeframe">An optional parameter specifying the timeframe for the posts (e.g., 'day', 'week', 'month'). Default is 'all'.</param>
    ''' <returns>Task representing the asynchronous operation, returning a JArray of posts.</returns>
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


    ''' <summary>
    ''' Asynchronously performs a search on Reddit for users, communities, or posts based on a query.
    ''' </summary>
    ''' <param name="searchType">The type of search to perform ('users', 'communities', or 'posts').</param>
    ''' <param name="query">The search query string.</param>
    ''' <param name="limit">The maximum number of search results to retrieve.</param>
    ''' <returns>Task representing the asynchronous operation, returning a JArray of search results.</returns>
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


    ''' <summary>
    ''' Asynchronously retrieves information about Reddit communities based on a specified type.
    ''' </summary>
    ''' <param name="communityType">The type of communities to retrieve (e.g., 'all', 'default', 'new', 'popular').</param>
    ''' <param name="limit">The maximum number of communities to retrieve.</param>
    ''' <returns>Task representing the asynchronous operation, returning a JArray of community information.</returns>
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
