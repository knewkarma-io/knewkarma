Imports System.Reflection
Imports System.Windows.Forms.VisualStyles.VisualStyleElement.StartPanel
Imports Newtonsoft.Json
Imports Newtonsoft.Json.Linq

Public Class DataGridViewer


    ''' <summary>
    ''' Privately shared instance of ApiHandler to be used by methods in this class for interacting with the GitHub API.
    ''' </summary>
    Private Shared ReadOnly apiHandler As New ApiHandler()

    ''' <summary>
    ''' Populates a DataGridView with data from a JSON object or a JSON array. 
    ''' For a single JSON object, it populates the DataGridView with two columns 'Key' and 'Value'.
    ''' For a JSON array, each object in the array becomes a row with object properties as columns.
    ''' </summary>
    ''' <param name="dataGridView">The DataGridView to be populated.</param>
    ''' <param name="jsonData">The JSON data, either a JObject or a JArray.</param>
    Private Shared Sub PopulateDataGridViewFromJson(ByRef dataGridView As DataGridView, ByVal jsonData As JToken)
        ' Clear existing columns and rows
        dataGridView.Columns.Clear()
        dataGridView.Rows.Clear()

        If TypeOf jsonData Is JArray Then
            ' Handle as an array of objects (multiple rows)
            Dim firstItem As Boolean = True
            For Each item As JObject In jsonData
                If firstItem Then
                    ' Add columns based on the first item
                    For Each prop In item.Properties()
                        dataGridView.Columns.Add(prop.Name, prop.Name)
                    Next
                    firstItem = False
                End If
                AddRowFromJObject(dataGridView, item)
            Next
        ElseIf TypeOf jsonData Is JObject Then
            ' Handle as a single object (populate with 'Key' and 'Value' columns)
            dataGridView.Columns.Add("Key", "Key")
            dataGridView.Columns.Add("Value", "Value")
            For Each prop As JProperty In CType(jsonData, JObject).Properties()
                dataGridView.Rows.Add(prop.Name, prop.Value.ToString())
            Next
        End If
    End Sub

    ''' <summary>
    ''' Adds a row to the DataGridView from a JObject.
    ''' </summary>
    ''' <param name="dataGridView">The DataGridView to be updated.</param>
    ''' <param name="jObject">The JObject containing the data for the row.</param>
    Private Shared Sub AddRowFromJObject(ByRef dataGridView As DataGridView, ByVal jObject As JObject)
        ' Create a new row
        Dim row As DataGridViewRow = New DataGridViewRow()
        row.CreateCells(dataGridView)

        ' Populate the row
        Dim columnIndex As Integer = 0
        For Each prop In jObject.Properties()
            row.Cells(columnIndex).Value = prop.Value.ToString()
            columnIndex += 1
        Next

        dataGridView.Rows.Add(row)
    End Sub


    Public Shared Async Function AsyncLoadListingsPosts(sort As String, limit As Integer) As Task
        Dim RawPosts As JArray = Nothing
        Dim PostsList As New JArray
        Dim listing As String = String.Empty

        If MainWindow.RadioButtonBest.Checked Then
            listing = MainWindow.RadioButtonBest.Text
        ElseIf MainWindow.RadioButtonRising.Checked Then
            listing = MainWindow.RadioButtonRising.Text
        ElseIf MainWindow.RadioButtonControversial.Checked Then
            listing = MainWindow.RadioButtonControversial.Text
        ElseIf MainWindow.RadioButtonPopular.Checked Then
            listing = MainWindow.RadioButtonPopular.Text
        End If

        RawPosts = Await apiHandler.AsyncGetPosts(
            type:="listing",
            from:=listing,
            sort:=sort,
            limit:=limit
        )


        For Each Post As JObject In RawPosts
            PostsList.Add(Post("data"))
        Next

        PopulateDataGridViewFromJson(dataGridView:=PostsWindow.DataGridPosts, jsonData:=PostsList)
        PostsWindow.Text = $"Posts — {listing} - {sort} {limit} posts"
        PostsWindow.Show()

        ' Prompt to save data if the conditions are met.
        CoreUtils.PromptSaveData(data:=RawPosts, title:=$"{listing} posts")
    End Function


    ''' <summary>
    ''' Asynchronously gets the user profile data and updates the DataGridView in the FormUserProfile form with it.
    ''' </summary>
    ''' <param name="username">The username to get the data for.</param>
    Private Shared Async Function AsyncLoadUserProfile(username As String) As Task
        Dim ProfileData As JObject = Await apiHandler.AsyncGetProfile(type:="user", from:=username)
        PopulateDataGridViewFromJson(dataGridView:=ProfileWindow.DataGridProfile, jsonData:=ProfileData)
        ProfileWindow.Text = $"User — {username}"
        ProfileWindow.Show()
        ' Get the user subreddit data from the user's profile data.
        ' LoadUserCommunity(UserCommunityData:=ProfileData)

        ' Prompt to save data if the conditions are met.
        CoreUtils.PromptSaveData(data:=ProfileData, $"User ({username}) profile")

    End Function


    ''' <summary>
    ''' Asynchronously loads the posts of a specific user and updates the DataGridView in the Posts.form.
    ''' </summary>
    ''' <param name="username">The Reddit username for which to fetch post data.</param>
    ''' <param name="form">The Posts.object that contains the DataGridView to be updated.</param>
    ''' <returns>A Task representing the asynchronous operation.</returns>
    Private Shared Async Function AsyncLoadUserPosts(
                                                    username As String,
                                                    sortCriterion As String,
                                                    postsLimit As Integer
                                                ) As Task
        Dim sort As String = MainWindow.ComboBoxUserDataListing.Text
        Dim limit As Integer = MainWindow.NumericUpDownUserDataLimit.Value


        Dim RawPosts As JArray = Await apiHandler.AsyncGetPosts(
            type:="user_posts",
            from:=username,
            sort:=sortCriterion,
            limit:=postsLimit
          )
        Dim isValid As Boolean = CoreUtils.IsValidData(data:=RawPosts)

        ' If the API data is valid, setup a DataGridView for the Posts.
        If isValid Then
            Dim PostsList As New JArray
            For Each Post As JObject In RawPosts
                PostsList.Add(Post("data"))
            Next

            PopulateDataGridViewFromJson(dataGridView:=PostsWindow.DataGridPosts, jsonData:=PostsList)
            PostsWindow.Text = $"User — {username} - {sort} {limit} posts"
            PostsWindow.Show()

            CoreUtils.PromptSaveData(data:=RawPosts, title:=$"User ({username}) posts")
        End If
    End Function


    ''' <summary>
    ''' Asynchronously loads the comments of a specific user and updates the DataGridView in the Comments.form.
    ''' </summary>
    ''' <param name="username">The Reddit username for which to fetch comments' data.</param>
    ''' <param name="form">The Comments.object that contains the DataGridView to be updated.</param>
    ''' <returns>A Task representing the asynchronous operation.</returns>
    Private Shared Async Function AsyncLoadUserComments(
                                                       username As String,
                                                       sortCriterion As String,
                                                       commentsLimit As Integer
                                                   ) As Task

        Dim RawComments As JArray = Await apiHandler.AsyncGetPosts(
            type:="user_comments",
            from:=username,
            sort:=sortCriterion,
            limit:=commentsLimit
        )
        Dim isValid As Boolean = CoreUtils.IsValidData(data:=RawComments)

        ' If the API data is valid, setup a DataGridView for the Posts.
        If isValid Then
            Dim CommentsList As New JArray
            For Each Comment As JObject In RawComments
                CommentsList.Add(Comment("data"))
            Next

            PopulateDataGridViewFromJson(dataGridView:=PostsWindow.DataGridPosts, jsonData:=CommentsList)
            PostsWindow.Text = $"User — {username} - {sortCriterion} {commentsLimit} comments"
            PostsWindow.Show()

            ' Prompt to save data if the conditions are met.
            CoreUtils.PromptSaveData(data:=RawComments, title:=$"User ({username}) comments")
        End If
    End Function

    ''' <summary>
    ''' Asynchronously load a user's data and update either the FormProfile, Posts.or FormUserComments forms 
    ''' depending on which Radio Button is checked.
    ''' </summary>
    ''' <param name="username">The username to fetch data for.</param>
    Public Shared Async Function AsyncLoadUserData(username As String) As Task
        If MainWindow.RadioButtonUserProfile.Checked Then
            Await AsyncLoadUserProfile(username:=username)
        ElseIf MainWindow.RadioButtonUserPosts.Checked Then
            Await AsyncLoadUserPosts(
                username:=username,
                sortCriterion:=MainWindow.ComboBoxUserDataListing.Text,
                postsLimit:=MainWindow.NumericUpDownUserDataLimit.Value
            )
        ElseIf MainWindow.RadioButtonUserComments.Checked Then
            Await AsyncLoadUserComments(
                username:=username,
                sortCriterion:=MainWindow.ComboBoxUserDataListing.Text,
                commentsLimit:=MainWindow.NumericUpDownUserDataLimit.Value
            )
        End If
    End Function

    ''' <summary>
    ''' Asynchronously load a subreddit's profile data and updates the Profile form.
    ''' </summary>
    ''' <param name="username">The username to fetch data for.</param>
    Public Shared Async Function CommunityProfile(subreddit As String) As Task
        Dim ProfileData As JObject = Await apiHandler.AsyncGetProfile(type:="community", from:=subreddit)

        PopulateDataGridViewFromJson(dataGridView:=ProfileWindow.DataGridProfile, jsonData:=ProfileData)
        ProfileWindow.Text = $"Community — {subreddit}"
        ProfileWindow.Show()

        ' Prompt to save data if the conditions are met.
        CoreUtils.PromptSaveData(data:=ProfileData, title:=$"Community ({subreddit}) profile")

    End Function


    ''' <summary>
    ''' Asynchronously loads the posts of a specific subreddit and updates the DataGridView in the Posts.form.
    ''' </summary>
    ''' <param name="subreddit">The Community for which to fetch post data.</param>
    ''' <param name="form">The Posts.object that contains the DataGridView to be updated.</param>
    ''' <returns>A Task representing the asynchronous operation.</returns>
    Private Shared Async Function AsyncLoadCommunityPosts(
                                                subreddit As String,
                                                sortCriterion As String,
                                                postsLimit As Integer
                                            ) As Task
        Dim RawPosts As JArray = Await apiHandler.AsyncGetPosts(
            type:="community",
            from:=subreddit,
            sort:=sortCriterion,
            limit:=postsLimit
        )
        Dim isValid As Boolean = CoreUtils.IsValidData(data:=RawPosts)

        ' If the API data is valid, setup a DataGridView for the Posts.
        If isValid Then
            Dim PostsList As New JArray

            For Each post As JObject In RawPosts
                PostsList.Add(post("data"))
            Next

            PopulateDataGridViewFromJson(dataGridView:=PostsWindow.DataGridPosts, jsonData:=PostsList)
            PostsWindow.Text = $"Community — {sortCriterion} {postsLimit} posts from r/{subreddit}"
            PostsWindow.Show()

            ' Prompt to save data if the conditions are met.
            CoreUtils.PromptSaveData(data:=RawPosts, title:=$"Community ({subreddit}) posts")
        End If
    End Function

    ''' <summary>
    ''' Asynchronously load a subreddit's data and update either the FormCommunityProfile or Posts.or forms 
    ''' depending on which Radio Button is checked.
    ''' </summary>
    ''' <param name="subreddit">The username to fetch data for.</param>
    Public Shared Async Function LoadCommunityDataAsync(subreddit As String) As Task
        If MainWindow.RadioButtonCommunityProfile.Checked Then
            Await CommunityProfile(subreddit:=subreddit)
        ElseIf MainWindow.RadioButtonCommunityPosts.Checked Then
            Await AsyncLoadCommunityPosts(
                subreddit:=subreddit,
                sortCriterion:=MainWindow.ComboBoxCommunityPostsListing.Text,
                postsLimit:=MainWindow.NumericUpDownCommunityPostsLimit.Value
            )
        End If
    End Function

    ''' <summary>
    ''' Asynchronously loads the posts of a specific user and updates the DataGridView on the given form.
    ''' </summary>
    ''' <param name="username">The Reddit username for which to fetch post data.</param>
    ''' <param name="form">The Posts.object that contains the DataGridView to be updated.</param>
    ''' <returns>A Task representing the asynchronous operation.</returns>
    Public Shared Async Function LoadSearchResultsAsync(
                                                       query As String,
                                                      limit As Integer
                                                   ) As Task
        Dim Results As JArray = Nothing
        If MainWindow.RadioButtonSearchUsers.Checked Then
            Results = Await apiHandler.AsyncSearch(searchType:="users", query:=query, limit:=limit)
        ElseIf MainWindow.RadioButtonSearchPosts.Checked Then
            Results = Await apiHandler.AsyncSearch(searchType:="posts", query:=query, limit:=limit)
        ElseIf MainWindow.RadioButtonSearchCommunities.Checked Then
            Results = Await apiHandler.AsyncSearch(searchType:="communities", query:=query, limit:=limit)
        End If

        Dim isValid As Boolean = CoreUtils.IsValidData(data:=Results)

        If isValid Then
            Dim ResultsList As New JArray
            For Each Result As JObject In Results
                ResultsList.Add(Result("data"))
            Next

            PopulateDataGridViewFromJson(dataGridView:=PostsWindow.DataGridPosts, jsonData:=ResultsList)
            PostsWindow.Text = $"Results — {query} - {limit} results"
            PostsWindow.Show()

            CoreUtils.PromptSaveData(data:=Results, title:=$"{query} Search Results")
        End If
    End Function

    ''' <summary>
    ''' Asynchronously loads the posts from the Reddit front page and updates the DataGridView in the Posts.form.
    ''' </summary>
    ''' <param name="form">The Posts.object that contains the DataGridView to be updated.</param>
    ''' <returns>A Task representing the asynchronous operation.</returns>
    Public Shared Async Function LoadFrontPagePostsAsync(
                                                        form As PostsWindow,
                                                        sortCriterion As String,
                                                        postsLimit As Integer
                                                    ) As Task
        Dim sort As String = MainWindow.ComboBoxFrontPageDataListing.Text
        Dim limit As Integer = MainWindow.NumericUpDownFrontPageDataLimit.Value

        Dim RawPosts As JArray = Await apiHandler.AsyncGetPosts(
            type:="front_page_posts",
            sort:=sortCriterion,
            limit:=postsLimit)
        Dim isValid As Boolean = CoreUtils.IsValidData(data:=RawPosts)

        ' If the API data is valid, setup a DataGridView for the Posts.
        If isValid Then
            Dim PostsList As New JArray
            For Each Post As JObject In RawPosts
                PostsList.Add(Post("data"))
            Next

            PopulateDataGridViewFromJson(dataGridView:=PostsWindow.DataGridPosts, jsonData:=PostsList)
            PostsWindow.Text = $"Posts — Front-Page - {sortCriterion} {postsLimit} posts"
            PostsWindow.Show()

            CoreUtils.PromptSaveData(data:=RawPosts, title:="Front-Page Posts")
        End If
    End Function
End Class