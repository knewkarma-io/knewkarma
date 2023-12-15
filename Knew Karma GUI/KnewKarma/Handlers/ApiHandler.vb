Imports System.Net.Http
Imports Newtonsoft.Json.Linq
Imports System.Runtime.InteropServices


''' <summary>
''' Class for making API calls to Reddit and or GitHub.
''' </summary>
Public Class ApiHandler
    ' Base Reddit endpoint
    Private Const BASE_ENDPOINT As String = "https://www.reddit.com"

    ''' <summary>
    ''' Represents the current program version in format {Major}.{Minor}.
    ''' </summary>
    Private ReadOnly appVersion As String = $"{My.Application.Info.Version.Major}.{My.Application.Info.Version.Minor}"

    ''' <summary>
    ''' Represents the .NET version program is running on.
    ''' </summary>
    Private ReadOnly dotNetVersion As String = RuntimeInformation.FrameworkDescription

    ''' <summary>
    ''' Makes an asynchronous GET request to a given endpoint.
    ''' </summary>
    ''' <param name="endpoint">The API endpoint URL.</param>
    ''' <returns>JToken received from the API call.</returns>
    Public Async Function AsyncGetData(endpoint As String) As Task(Of JToken)
        Try
            Using httpClient As New HttpClient()
                httpClient.DefaultRequestHeaders.Add(
                    "User-Agent",
                    $"Knew-Karma/{appVersion} ({dotNetVersion}; +https://rly0nheart.github.io)"
                )

                Dim response As HttpResponseMessage = Await httpClient.GetAsync(endpoint)

                If response.IsSuccessStatusCode Then
                    Dim json As String = Await response.Content.ReadAsStringAsync()
                    Return JObject.Parse(json)
                Else
                    MessageBox.Show(
                        response.ReasonPhrase,
                        "An API Error occurred",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Error
                    )
                    Return Nothing
                End If
            End Using
        Catch ex As Exception
            MessageBox.Show(
                ex.Message,
                "An HTTP Error occurred",
                MessageBoxButtons.OK,
                MessageBoxIcon.Error
            )
        End Try
        Return Nothing
    End Function

    ''' <summary>
    ''' Asynchronously fetches the program's update information from GitHub.
    ''' <summary>
    Public Async Function AsyncGetUpdates() As Task
        AboutWindow.Version.Text = "Checking for updates..."
        ' Making an asynchronous request to check for updates.
        Dim data As JObject = Await AsyncGetData(endpoint:="https://api.github.com/repos/rly0nheart/knewkarma/releases/latest")

        ' Checking if data is not null before proceeding with extracting information from it.
        If data IsNot Nothing Then
            ' Extracting the tag name, body, and HTML URL from the data.
            Dim tagName As String = data("tag_name")?.ToString

            ' Checking if the current version is the latest version.
            If tagName = My.Application.Info.Version.ToString Then
                AboutWindow.Version.Text = $"Up-to-date: {My.Application.Info.Version}"
            Else
                AboutWindow.Version.Text = $"Updates found: {tagName}"
                AboutWindow.ButtonGetUpdates.Enabled = True
            End If
        End If
    End Function


    ''' <summary>
    ''' Asynchronously retrieves profile data from a specified source.
    ''' </summary>
    ''' <param name="profileType">The type of profile to retrieve.</param>
    ''' <param name="profileSource">The source from where the profile should be fetched (e.g., specific user or subreddit).</param>
    ''' <returns>A Task(Of JObject) representing the asynchronous operation, which upon completion returns a Jobject of profile data.</returns>
    Public Async Function AsyncGetProfile(
                                         profileType As String, profileSource As String) As Task(Of JObject)
        Dim profileTypeMap As New List(Of Tuple(Of String, String)) From {
            Tuple.Create("user_profile", $"{BASE_ENDPOINT}/user/{profileSource}/about.json"),
            Tuple.Create("subreddit_profile", $"{BASE_ENDPOINT}/r/{profileSource}/about.json")
        }

        Dim profileEndpoint As String = Nothing

        For Each Type In profileTypeMap
            If Type.Item1 = profileType Then
                profileEndpoint = Type.Item2
                Exit For
            End If
        Next

        Dim profile As JObject = Await AsyncGetData(endpoint:=profileEndpoint)

        Return If(profile IsNot Nothing AndAlso profile?("data") IsNot Nothing, profile?("data"), New JObject())
    End Function


    ''' <summary>
    ''' Asynchronously retrieves posts from a specified source with pagination.
    ''' </summary>
    ''' <param name="sortCriterion">The criterion by which the posts should be sorted.</param>
    ''' <param name="postsLimit">The limit on the number of posts to retrieve.</param>
    ''' <param name="postsType">The type of posts to retrieve (e.g., user_posts, user_comments).</param>
    ''' <param name="postsSource">The source from where the posts should be fetched (e.g., specific user or subreddit).</param>
    ''' <returns>A Task(Of JArray) representing the asynchronous operation, which upon completion returns a JArray of posts.</returns>
    Public Async Function AsyncGetPosts(
                                       ByVal sortCriterion As String,
                                       ByVal postsLimit As Integer,
                                       ByVal postsType As String,
                                       Optional ByVal postsSource As String = Nothing
                                   ) As Task(Of JArray)
        Dim postsTypeMap As New Dictionary(Of String, String) From {
            {"user_posts", $"{BASE_ENDPOINT}/user/{postsSource}/submitted.json?sort={sortCriterion}&limit={postsLimit}"},
            {"user_comments", $"{BASE_ENDPOINT}/user/{postsSource}/comments.json?sort={sortCriterion}&limit={postsLimit}"},
            {"subreddit_posts", $"{BASE_ENDPOINT}/r/{postsSource}.json?sort={sortCriterion}&limit={postsLimit}"},
            {"search_posts", $"{BASE_ENDPOINT}/search.json?q={postsSource}&sort={sortCriterion}&limit={postsLimit}"},
            {"listing_posts", $"{BASE_ENDPOINT}/r/{postsSource}.json?sort={sortCriterion}&limit={postsLimit}"},
            {"front_page_posts", $"{BASE_ENDPOINT}/.json?sort={sortCriterion}&limit={postsLimit}"}
        }

        If Not postsTypeMap.ContainsKey(postsType) Then
            Throw New ArgumentException($"Invalid post type: {postsType}")
        End If

        Dim postsEndpoint As String = postsTypeMap(postsType)
        Dim allPosts As New JArray()
        Dim lastPostId As String = String.Empty
        Dim paginatePosts As Boolean = postsLimit > 100

        While allPosts.Count < postsLimit
            Dim paginationEndpoint As String = If(paginatePosts And Not String.IsNullOrEmpty(lastPostId), $"{postsEndpoint}&after={lastPostId}", postsEndpoint)
            Dim postsData As JObject = Await AsyncGetData(endpoint:=paginationEndpoint)
            Dim postsChildren As JArray = postsData("data")("children")

            If postsChildren.Count = 0 Then
                Exit While
            End If

            allPosts.Merge(postsChildren)

            lastPostId = postsChildren.Last("data")("id").ToString()
        End While

        Return allPosts
    End Function
End Class

