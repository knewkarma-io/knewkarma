Imports Newtonsoft.Json.Linq

Public Class DataGridViewer


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

        PopulateDataGridViewFromJson(dataGridView:=DataWindow.DataGrid, jsonData:=PostsList)
        DataWindow.Text = $"Posts — {listing} - {sort} {limit} posts"
        DataWindow.Show()

        ' Prompt to save data if the conditions are met.
        CoreUtils.PromptSaveData(data:=RawPosts, title:=$"{listing} posts")
    End Function



    Private Shared Async Function AsyncLoadProfile(profileType As String, profileSource As String) As Task
        Dim ProfileData As JObject = Await apiHandler.AsyncGetProfile(type:=profileType.ToLowerInvariant, from:=profileSource)

        PopulateDataGridViewFromJson(dataGridView:=DataWindow.DataGrid, jsonData:=ProfileData)

        DataWindow.Size = New Size(360, 462)
        DataWindow.MaximizeBox = False
        DataWindow.FormBorderStyle = FormBorderStyle.FixedSingle
        DataWindow.Text = $"{profileType} — {profileSource}"
        DataWindow.Show()

        ' Prompt to save data if the conditions are met.
        CoreUtils.PromptSaveData(data:=ProfileData, $"{profileType} ({profileSource}) profile")

    End Function


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

            PopulateDataGridViewFromJson(dataGridView:=DataWindow.DataGrid, jsonData:=PostsList)

            DataWindow.Text = $"User — {username} - {sort} {limit} posts"
            DataWindow.Show()

            CoreUtils.PromptSaveData(data:=RawPosts, title:=$"User ({username}) posts")
        End If
    End Function


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

            PopulateDataGridViewFromJson(dataGridView:=DataWindow.DataGrid, jsonData:=CommentsList)

            DataWindow.Size = New Size(466, 366)
            DataWindow.Text = $"User — {username} - {sortCriterion} {commentsLimit} comments"
            DataWindow.Show()

            ' Prompt to save data if the conditions are met.
            CoreUtils.PromptSaveData(data:=RawComments, title:=$"User ({username}) comments")
        End If
    End Function


    Public Shared Async Function AsyncLoadUserData(username As String) As Task
        If MainWindow.RadioButtonUserProfile.Checked Then
            Await AsyncLoadProfile(profileType:="User", profileSource:=username)
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



    Private Shared Async Function AsyncLoadCommunityPosts(
                                                community As String,
                                                sortCriterion As String,
                                                postsLimit As Integer
                                            ) As Task
        Dim RawPosts As JArray = Await apiHandler.AsyncGetPosts(
            type:="community",
            from:=community,
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

            PopulateDataGridViewFromJson(dataGridView:=DataWindow.DataGrid, jsonData:=PostsList)
            DataWindow.Text = $"Community — {sortCriterion} {postsLimit} posts from r/{community}"
            DataWindow.Show()

            ' Prompt to save data if the conditions are met.
            CoreUtils.PromptSaveData(data:=RawPosts, title:=$"Community ({community}) posts")
        End If
    End Function


    Public Shared Async Function LoadCommunityDataAsync(community As String) As Task
        If MainWindow.RadioButtonCommunityProfile.Checked Then
            Await AsyncLoadProfile(profileType:="community", profileSource:=community)
        ElseIf MainWindow.RadioButtonCommunityPosts.Checked Then
            Await AsyncLoadCommunityPosts(
                community:=community,
                sortCriterion:=MainWindow.ComboBoxCommunityPostsListing.Text,
                postsLimit:=MainWindow.NumericUpDownCommunityPostsLimit.Value
            )
        End If
    End Function


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

            PopulateDataGridViewFromJson(dataGridView:=DataWindow.DataGrid, jsonData:=ResultsList)
            DataWindow.Text = $"Results — {query} - {limit} results"
            DataWindow.Show()

            CoreUtils.PromptSaveData(data:=Results, title:=$"{query} Search Results")
        End If
    End Function


    Public Shared Async Function LoadFrontPageAndNewPostsAsync(
                                                        form As DataWindow,
                                                        sortCriterion As String,
                                                        postsLimit As Integer
                                                    ) As Task
        Dim sort As String = MainWindow.ComboBoxFrontPageAndNewPostsListing.Text
        Dim limit As Integer = MainWindow.NumericUpDownFrontPageAndNewPostsLimit.Value

        Dim RawPosts As JArray = Nothing
        If MainWindow.RadioButtonNewPosts.Checked Then
            RawPosts = Await apiHandler.AsyncGetPosts(
                type:="new",
                sort:=sortCriterion,
                limit:=postsLimit
            )
        ElseIf MainWindow.RadioButtonFrontPagePosts.Checked Then
            RawPosts = Await apiHandler.AsyncGetPosts(
                type:="front_page",
                sort:=sortCriterion,
                limit:=postsLimit
            )
        End If

        Dim isValid As Boolean = CoreUtils.IsValidData(data:=RawPosts)

        ' If the API data is valid, setup a DataGridView for the Posts.
        If isValid Then
            Dim PostsList As New JArray
            For Each Post As JObject In RawPosts
                PostsList.Add(Post("data"))
            Next

            PopulateDataGridViewFromJson(dataGridView:=DataWindow.DataGrid, jsonData:=PostsList)
            DataWindow.Text = $"Posts - {sortCriterion} {postsLimit} posts"
            DataWindow.Show()

            CoreUtils.PromptSaveData(data:=RawPosts, title:="Posts")
        End If
    End Function
End Class