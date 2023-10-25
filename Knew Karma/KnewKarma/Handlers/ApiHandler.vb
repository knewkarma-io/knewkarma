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
                httpClient.DefaultRequestHeaders.Add("User-Agent", $"Knew-Karma/{appVersion} ({dotNetVersion}; +https://about.me/rly0nheart)")

                Dim response As HttpResponseMessage = Await httpClient.GetAsync(endpoint)

                If response.IsSuccessStatusCode Then
                    Dim json As String = Await response.Content.ReadAsStringAsync()
                    Return JObject.Parse(json)
                Else
                    MessageBox.Show(response.ReasonPhrase, "An API Error occurred", MessageBoxButtons.OK, MessageBoxIcon.Error)
                    Return Nothing
                End If
            End Using
        Catch ex As Exception
            MessageBox.Show(ex.Message, "An HTTP Error occurred", MessageBoxButtons.OK, MessageBoxIcon.Error)
        End Try
        Return Nothing
    End Function

    ''' <summary>
    ''' Asynchronously fetches the program's update information from GitHub.
    ''' <summary>
    Public Async Function AsyncGetUpdates() As Task(Of JObject)
        Return Await AsyncGetData(endpoint:="https://api.github.com/repos/bellingcat/knewkarma/releases/latest")
    End Function

    ''' <summary>
    ''' Asynchronously fetches a user's Reddit profile.
    ''' </summary>
    ''' <param name="username">The Reddit username.</param>
    ''' <returns>A JSON object containing the user's profile data.</returns>
    Public Async Function AsyncGetUserProfile(username As String) As Task(Of JObject)
        Dim data As JObject = Await AsyncGetData(endpoint:=$"{BASE_ENDPOINT}/user/{username}/about.json")
        Return If(data IsNot Nothing AndAlso data("data") IsNot Nothing, data("data"), New JObject())
    End Function

    ''' <summary>
    ''' Asynchronously fetches posts submitted by a user.
    ''' </summary>
    ''' <param name="username">The Reddit username.</param>
    ''' <param name="sort">Sorting criterion ('new', 'hot', etc.).</param>
    ''' <param name="limit">Number of posts to fetch.</param>
    ''' <returns>A JSON array containing the user's posts.</returns>
    Public Async Function AsyncGetUserPosts(username As String, sort As String, limit As Integer) As Task(Of JArray)
        Dim data As JObject = Await AsyncGetData(endpoint:=$"{BASE_ENDPOINT}/user/{username}/submitted.json?sort={sort}&limit={limit}")
        Return If(data IsNot Nothing AndAlso data("data") IsNot Nothing, data("data")?("children"), New JArray())
    End Function

    ''' <summary>
    ''' Asynchronously fetches comments submitted by a user.
    ''' </summary>
    ''' <param name="username">The Reddit username.</param>
    ''' <param name="sort">Sorting criterion ('new', 'hot', etc.).</param>
    ''' <param name="limit">Number of posts to fetch.</param>
    ''' <returns>A JSON array containing the user's posts.</returns>
    Public Async Function AsyncGetUserComments(username As String, sort As String, limit As Integer) As Task(Of JArray)
        Dim data As JObject = Await AsyncGetData(endpoint:=$"{BASE_ENDPOINT}/user/{username}/comments.json?sort={sort}&limit={limit}")
        Return If(data IsNot Nothing AndAlso data("data") IsNot Nothing, data("data")?("children"), New JArray())
    End Function

    ''' <summary>
    ''' Asynchronously fetches profile data for a subreddit.
    ''' </summary>
    ''' <param name="subreddit">The subreddit name.</param>
    ''' <returns>A JSON object containing the subreddit's profile data.</returns>
    Public Async Function AsyncGetSubredditProfile(subreddit As String) As Task(Of JObject)
        Dim data As JObject = Await AsyncGetData(endpoint:=$"{BASE_ENDPOINT}/r/{subreddit}/about.json")
        Return If(data IsNot Nothing AndAlso data("data") IsNot Nothing, data("data"), New JObject())
    End Function

    ''' <summary>
    ''' Asynchronously fetches posts in a subreddit.
    ''' </summary>
    ''' <param name="subreddit">The subreddit username.</param>
    ''' <param name="sort">Sorting criterion ('new', 'hot', etc.).</param>
    ''' <param name="limit">Number of posts to fetch.</param>
    ''' <returns>A JSON array containing the user's posts.</returns>
    Public Async Function AsyncGetSubredditPosts(subreddit As String, sort As String, limit As Integer) As Task(Of JArray)
        Dim data As JObject = Await AsyncGetData(endpoint:=$"{BASE_ENDPOINT}/r/{subreddit}.json?sort={sort}&limit={limit}")
        Return If(data IsNot Nothing AndAlso data("data") IsNot Nothing, data("data")?("children"), New JArray())
    End Function

    ''' <summary>
    ''' Asynchronously searches Reddit for a query string.
    ''' </summary>
    ''' <param name="query">The search query.</param>
    ''' <param name="sort">Sorting criterion ('new', 'hot', etc.).</param>
    ''' <param name="limit">Number of search results to fetch.</param>
    ''' <returns>A JSON array containing the search results.</returns>
    Public Async Function AsyncSearchPosts(query As String, sort As String, limit As Integer) As Task(Of JArray)
        Dim data As JObject = Await AsyncGetData(endpoint:=$"{BASE_ENDPOINT}/search.json?q={query}&sort={sort}&limit={limit}")
        Return If(data IsNot Nothing AndAlso data("data") IsNot Nothing, data("data")?("children"), New JArray())
    End Function

    ''' <summary>
    ''' Asynchronously gets posts from the Reddit front page.
    ''' </summary>
    ''' <param name="sort">Sorting criterion ('new', 'hot', etc.).</param>
    ''' <param name="limit">Number of search results to fetch.</param>
    ''' <returns>A JSON array containing the search results.</returns>
    Public Async Function AsyncGetFrontPagePosts(sort As String, limit As Integer) As Task(Of JArray)
        Dim data As JObject = Await AsyncGetData(endpoint:=$"{BASE_ENDPOINT}/.json?sort={sort}&limit={limit}")
        Return If(data IsNot Nothing AndAlso data("data") IsNot Nothing, data("data")?("children"), New JArray())
    End Function

    Public Async Function AsyncGetListingsPosts(sort As String, limit As Integer, listing As String) As Task(Of JArray)
        Dim data As JObject = Await AsyncGetData(endpoint:=$"{BASE_ENDPOINT}/r/{listing}.json?sort={sort}&limit={limit}")
        Return If(data IsNot Nothing AndAlso data("data") IsNot Nothing, data("data")?("children"), New JArray())
    End Function
End Class
