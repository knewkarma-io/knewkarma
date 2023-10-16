Imports System.Globalization

Public Class Main
    Public Shared ReadOnly settings As New SettingsManager()
    Private bytesSentCounter As PerformanceCounter
    Private bytesReceivedCounter As PerformanceCounter

    ''' <summary>
    ''' Event handler for the form load event.
    ''' It loads settings, toggles dark mode if necessary, checks for directories, logs first time launch, and sets the form title.
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">An EventArgs that contains the event data.</param>
    Private Sub MainWindow_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        CoreUtils.PathFinder()

        TreeView1.Nodes(0).Expand()
        TreeView1.Nodes(0).Text = Environment.UserName

        settings.LoadSettings()
        settings.ToggleSettings(enabled:=settings.DarkMode, saveTo:="darkmode")
        settings.ToggleSettings(enabled:=settings.SaveToJson, saveTo:="json")
        settings.ToggleSettings(enabled:=settings.SaveToCsv, saveTo:="csv")

        ComboBoxFrontPageDataListing.SelectedIndex = 0
        ComboBoxUserPostsListing.SelectedIndex = 0
        ComboBoxSearchResultListing.SelectedIndex = 0
        ComboBoxSubredditPostsListing.SelectedIndex = 0
        ComboBoxPostListingsListing.SelectedIndex = 0
        ComboBoxPostDataListing.SelectedIndex = 0
    End Sub

    Private Sub FormMain_HelpButtonClicked(sender As Object, e As System.ComponentModel.CancelEventArgs) Handles MyBase.HelpButtonClicked
        ' Cancel the default behavior (opening system help)
        e.Cancel = True
        Shell("cmd.exe /c start https://github.com/bellingcat/knewkarma/wiki")
    End Sub

    Private Sub ExitProgram()
        Dim result As DialogResult = MessageBox.Show("This will close the program, continue?", "Exit", MessageBoxButtons.YesNo, MessageBoxIcon.Question)
        If result = DialogResult.Yes Then
            Me.Close()
        End If
    End Sub

    ''' <summary>
    ''' Event handler for the 'About' menu item click.
    ''' It shows the 'About' box.
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">An EventArgs that contains the event data.</param>
    Private Sub ToolStripMenuItemAbout_Click(sender As Object, e As EventArgs) Handles AboutToolStripMenuItem.Click
        About.ShowDialog()
    End Sub

    ''' <summary>
    ''' Event handler for the 'Quit' menu item click.
    ''' It asks the user for confirmation and closes the program if the user agrees.
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">An EventArgs that contains the event data.</param>
    Private Sub ToolStripMenuItemExit_Click(sender As Object, e As EventArgs) Handles ExitToolStripMenuItem.Click
        ExitProgram()
    End Sub

    ''' <summary>
    ''' Handles the click event of the Search button.
    ''' Collects inputs, fetches Reddit posts based on the inputs,
    ''' and processes Reddit posts.
    ''' </summary>
    ''' <param name="sender">The sender of the event.</param>
    ''' <param name="e">The EventArgs instance containing the event data.</param>
    Private Async Sub ButtonSearch_Click(sender As Object, e As EventArgs) Handles ButtonSearch.Click
        Dim query As String = CheckInput(txtBox:=TextBoxQuery)
        If query IsNot Nothing Then
            Await DataGridViewer.LoadSearchResultsAsync(query:=query, form:=Posts)
        End If
    End Sub

    ''' <summary>
    ''' Handles the KeyDown event for the TextBoxQuery. 
    ''' Processes Reddit posts when the Enter key is pressed.
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">The <see cref="KeyEventArgs"/> instance containing the event data.</param>
    Private Async Sub TextBoxQuery_KeyDown(sender As Object, e As KeyEventArgs) Handles TextBoxQuery.KeyDown
        If e.KeyCode = Keys.Enter Then
            e.SuppressKeyPress = True
            Dim query As String = CheckInput(txtBox:=TextBoxQuery)
            If query IsNot Nothing Then
                Await DataGridViewer.LoadSearchResultsAsync(query:=query, form:=Posts)
            End If
        End If
    End Sub


    ''' <summary>
    ''' Handles the click event of ButtonUserGO.
    ''' Collects inputs, fetches Reddit posts based on the inputs,
    ''' and processes Reddit posts.
    ''' </summary>
    ''' <param name="sender">The sender of the event.</param>
    ''' <param name="e">The EventArgs instance containing the event data.</param>
    Private Async Sub ButtonFetchUserData_Click(sender As Object, e As EventArgs) Handles ButtonFetchUserData.Click
        Dim username As String = CheckInput(txtBox:=TextBoxUsername)
        If username IsNot Nothing Then
            Await DataGridViewer.AsyncLoadUserData(username:=username)
        End If
    End Sub

    ''' <summary>
    ''' Handles the KeyDown event of TextBoxUsername.
    ''' Collects inputs, fetches Reddit posts based on the inputs,
    ''' and processes Reddit posts.
    ''' </summary>
    ''' <param name="sender">The sender of the event.</param>
    ''' <param name="e">The EventArgs instance containing the event data.</param>
    Private Async Sub TextBoxUsername_KeyDown(sender As Object, e As KeyEventArgs) Handles TextBoxUsername.KeyDown
        If e.KeyCode = Keys.Enter Then
            e.SuppressKeyPress = True
            Dim username As String = CheckInput(txtBox:=TextBoxUsername)
            If username IsNot Nothing Then
                Await DataGridViewer.AsyncLoadUserData(username:=username)
            End If
        End If
    End Sub

    Private Async Sub NumericUpDownUserDataLimit_KeyDown(sender As Object, e As KeyEventArgs) Handles NumericUpDownUserDataLimit.KeyDown
        If e.KeyCode = Keys.Enter Then
            e.SuppressKeyPress = True
            Dim username As String = CheckInput(txtBox:=TextBoxUsername)
            If username IsNot Nothing Then
                Await DataGridViewer.AsyncLoadUserData(username:=username)
            End If
        End If
    End Sub

    ''' <summary>
    ''' Handles the Click event for the ButtonFetchSubredditData control. 
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">The <see cref="KeyEventArgs"/> instance containing the event data.</param>
    Private Async Sub ButtonFetchSubredditData_Click(sender As Object, e As EventArgs) Handles ButtonFetchSubredditData.Click
        Dim subreddit As String = CheckInput(txtBox:=TextBoxSubreddit)
        If subreddit IsNot Nothing Then
            Await DataGridViewer.LoadSubredditDataAsync(subreddit:=subreddit)
        End If
    End Sub

    ''' <summary>
    ''' Handles the KeyDown event for the TextBoxSubreddit. 
    ''' Processes Reddit posts when the Enter key is pressed.
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">The <see cref="KeyEventArgs"/> instance containing the event data.</param>
    Private Async Sub TextBoxSubreddit_KeyDown(sender As Object, e As KeyEventArgs) Handles TextBoxSubreddit.KeyDown
        If e.KeyCode = Keys.Enter Then
            e.SuppressKeyPress = True
            Dim subreddit As String = CheckInput(txtBox:=TextBoxSubreddit)
            If subreddit IsNot Nothing Then
                Await DataGridViewer.LoadSubredditDataAsync(subreddit:=subreddit)
            End If
        End If
    End Sub

    Private Async Sub NumericUpDownSubredditDataLimit_KeyDown(sender As Object, e As KeyEventArgs) Handles NumericUpDownSubredditDataLimit.KeyDown
        If e.KeyCode = Keys.Enter Then
            e.SuppressKeyPress = True
            Dim subreddit As String = CheckInput(txtBox:=TextBoxSubreddit)
            If subreddit IsNot Nothing Then
                Await DataGridViewer.LoadSubredditDataAsync(subreddit:=subreddit)
            End If
        End If
    End Sub


    ''' <summary>
    ''' Event handler for the 'Dark Mode' checkbox change event.
    ''' It toggles the dark mode of the application based on the checkbox status.
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">An EventArgs that contains the event data.</param>
    Private Sub ToolStripMenuItemDarkMode_CheckedChanged(sender As Object, e As EventArgs) Handles DarkModeToolStripMenuItem.CheckedChanged
        settings.ToggleSettings(enabled:=DarkModeToolStripMenuItem.Checked, saveTo:="darkmode")
    End Sub

    ''' <summary>
    ''' Event handler for the 'to CSV' checkbox change event.
    ''' It toggles the dark mode of the application based on the checkbox status.
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">An EventArgs that contains the event data.</param>
    Private Sub ToCSVToolStripMenuItem_CheckedChanged(sender As Object, e As EventArgs) Handles ToCSVToolStripMenuItem.CheckedChanged
        settings.ToggleSettings(enabled:=ToCSVToolStripMenuItem.Checked, saveTo:="csv")
    End Sub

    ''' <summary>
    ''' Event handler for the 'to JSON' checkbox change event.
    ''' It toggles the dark mode of the application based on the checkbox status.
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">An EventArgs that contains the event data.</param>
    Private Sub ToJSONToolStripMenuItem_CheckedChanged(sender As Object, e As EventArgs) Handles ToJSONToolStripMenuItem.CheckedChanged
        settings.ToggleSettings(enabled:=ToJSONToolStripMenuItem.Checked, saveTo:="json")
    End Sub

    ''' <summary>
    ''' Handles the Click event for the ButtonFetchFrontPageData control. 
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">The <see cref="KeyEventArgs"/> instance containing the event data.</param>
    Private Async Sub ButtonFetchFrontPageData_Click(sender As Object, e As EventArgs) Handles ButtonFetchFrontPageData.Click
        Await DataGridViewer.LoadFrontPagePostsAsync(form:=Posts)
    End Sub


    Private Async Sub NumericUpDownFrontPageDataLimit_KeyDown(sender As Object, e As KeyEventArgs) Handles NumericUpDownFrontPageDataLimit.KeyDown
        If e.KeyCode = Keys.Enter Then
            e.SuppressKeyPress = True
            Await DataGridViewer.LoadFrontPagePostsAsync(form:=Posts)
        End If
    End Sub

    ''' <summary>
    ''' Handles the Click event for the ButtonFetchPostListingsData control. 
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">The <see cref="KeyEventArgs"/> instance containing the event data.</param>
    Private Async Sub ButtonFetchPostListingsData_Click(sender As Object, e As EventArgs)
        Await DataGridViewer.AsyncLoadListingsPosts(sort:=ComboBoxPostListingsListing.Text, limit:=NumericUpDownPostListingsLimit.Value)
    End Sub

    ''' <summary>
    ''' Checks if an input text box is empty or contains only white spaces.
    ''' </summary>
    ''' <returns>A nullable String containing the username if it's not empty or white-space, otherwise returns Nothing.</returns>
    Private Shared Function CheckInput(txtBox As TextBox) As String
        If Not String.IsNullOrWhiteSpace(txtBox.Text) Then
            Return txtBox.Text
        Else
            MessageBox.Show("Input cannot be empty or consist only of white spaces.", "Warning", MessageBoxButtons.OK, MessageBoxIcon.Warning)
            txtBox.Clear()
            Return Nothing
        End If
    End Function

    Private Sub HideAllPanels()
        For Each ctrl As Control In Me.Controls
            If TypeOf ctrl Is Panel Then
                ctrl.Visible = False
            End If
        Next
    End Sub

    Private Sub TreeView1_AfterSelect(sender As Object, e As TreeViewEventArgs) Handles TreeView1.AfterSelect

        HideAllPanels()
        Me.Width = 393 ' Set the Window's width to 393 (normal width)
        Me.Text = My.Application.Info.AssemblyName
        Select Case e.Node.Text
            Case "Post (N/A)"
                PanelPostData.Visible = True
            Case "User"
                PanelUserData.Visible = True
            Case "Subreddit"
                PanelSubredditData.Visible = True
            Case "Search"
                PanelSearchPosts.Visible = True
            Case "Listings"
                PanelPostListings.Visible = True
            Case "Front Page"
                PanelFrontPageData.Visible = True
            Case Else
                Me.Width = 169 ' Set the Window's width to 169
                Me.Text = ""
        End Select
    End Sub

    ''' <summary>
    ''' Handles the MouseEnter event for a ToolStripMenuItem.
    ''' </summary>
    ''' <param name="sender">The source of the event, the ToolStripMenuItem that is being hovered over.</param>
    ''' <param name="e">An EventArgs that contains the event data.</param>
    ''' <param name="color">A dictionary containing the color settings to be applied.</param>
    Public Shared Sub OnMenuItemMouseEnter(sender As Object, e As EventArgs, ByVal color As Dictionary(Of String, Color))
        ' Convert the sender to a ToolStripMenuItem
        Dim item As ToolStripMenuItem = CType(sender, ToolStripMenuItem)

        ' Set the foreground color from the color dictionary
        item.ForeColor = color("MenuItemMouseEnterColor")
    End Sub

    ''' <summary>
    ''' Handles the MouseLeave event for a ToolStripMenuItem.
    ''' </summary>
    ''' <param name="sender">The source of the event, the ToolStripMenuItem that the mouse left.</param>
    ''' <param name="e">An EventArgs that contains the event data.</param>
    ''' <param name="color">A dictionary containing the color settings to be applied.</param>
    Public Shared Sub OnMenuItemMouseLeave(sender As Object, e As EventArgs, ByVal color As Dictionary(Of String, Color))
        ' Convert the sender to a ToolStripMenuItem
        Dim item As ToolStripMenuItem = CType(sender, ToolStripMenuItem)

        ' Set the foreground color from the color dictionary
        item.ForeColor = color("PrimaryTextColor")
    End Sub

    ''' <summary>
    ''' Handles the CheckedChanged event for the RadioButtonUserProfile control. 
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">The <see cref="KeyEventArgs"/> instance containing the event data.</param>
    Private Sub RadioButtonUserProfile_CheckedChanged(sender As Object, e As EventArgs) Handles RadioButtonUserProfile.CheckedChanged
        CoreUtils.HandleRadioButtonChanges(form:=Me)
    End Sub

    ''' <summary>
    ''' Handles the CheckedChanged event for the RadioButtonUserPosts control. 
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">The <see cref="KeyEventArgs"/> instance containing the event data.</param>
    Private Sub RadioButtonUserPosts_CheckedChanged(sender As Object, e As EventArgs) Handles RadioButtonUserPosts.CheckedChanged
        CoreUtils.HandleRadioButtonChanges(form:=Me)
    End Sub

    ''' <summary>
    ''' Handles the CheckedChanged event for the RadioButtonUserComments control. 
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">The <see cref="KeyEventArgs"/> instance containing the event data.</param>
    Private Sub RadioButtonUserComments_CheckedChanged(sender As Object, e As EventArgs) Handles RadioButtonUserComments.CheckedChanged
        CoreUtils.HandleRadioButtonChanges(form:=Me)
    End Sub

    ''' <summary>
    ''' Handles the CheckedChanged event for the RadioButtonSubredditProfile control. 
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">The <see cref="KeyEventArgs"/> instance containing the event data.</param>
    Private Sub RadioButtonSubredditProfile_CheckedChanged(sender As Object, e As EventArgs) Handles RadioButtonSubredditProfile.CheckedChanged
        CoreUtils.HandleRadioButtonChanges(form:=Me)
    End Sub

    ''' <summary>
    ''' Handles the CheckedChanged event for the RadioButtonSubredditPosts control. 
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">The <see cref="KeyEventArgs"/> instance containing the event data.</param>
    Private Sub RadioButtonSubredditPosts_CheckedChanged(sender As Object, e As EventArgs) Handles RadioButtonSubredditPosts.CheckedChanged
        CoreUtils.HandleRadioButtonChanges(form:=Me)
    End Sub

    ''' <summary>
    ''' Handles the CheckedChanged event for the RadioButtonPostProfile control. 
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">The <see cref="KeyEventArgs"/> instance containing the event data.</param>
    Private Sub RadioButtonPostProfile_CheckedChanged(sender As Object, e As EventArgs) Handles RadioButtonPostProfile.CheckedChanged
        CoreUtils.HandleRadioButtonChanges(form:=Me)
    End Sub

    ''' <summary>
    ''' Handles the CheckedChanged event for the RadioButtonPostComments control. 
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">The <see cref="KeyEventArgs"/> instance containing the event data.</param>
    Private Sub RadioButtonPostComments_CheckedChanged(sender As Object, e As EventArgs) Handles RadioButtonPostComments.CheckedChanged
        CoreUtils.HandleRadioButtonChanges(form:=Me)
    End Sub

    Private Async Sub NumericUpDownPostListingsLimit_KeyDown(sender As Object, e As KeyEventArgs) Handles NumericUpDownPostListingsLimit.KeyDown
        If e.KeyCode = Keys.Enter Then
            e.SuppressKeyPress = True
            Await DataGridViewer.AsyncLoadListingsPosts(sort:=ComboBoxPostListingsListing.Text, limit:=NumericUpDownPostListingsLimit.Value)
        End If
    End Sub

    ''' <summary>
    ''' Handles the Click event for the ButtonFetchPostListings control. 
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">The <see cref="KeyEventArgs"/> instance containing the event data.</param>
    Private Async Sub ButtonFetchPostListings_Click(sender As Object, e As EventArgs) Handles ButtonFetchPostListings.Click
        Await DataGridViewer.AsyncLoadListingsPosts(sort:=ComboBoxPostListingsListing.Text, limit:=NumericUpDownPostListingsLimit.Value)
    End Sub

    ''' <summary>
    ''' Handles the CheckedChanged event of DarkModeEnableToolStripMenuItem.
    ''' If DarkModeEnableToolStripMenuItem is checked, DarkMode is enabled,
    ''' DarkModeDisableToolStripMenuItem is unchecked, and the settings are saved and applied.
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">The EventArgs instance containing the event data.</param>
    Private Sub DarkModeEnableToolStripMenuItem_CheckedChanged(sender As Object, e As EventArgs) Handles DarkModeEnableToolStripMenuItem.CheckedChanged
        If DarkModeEnableToolStripMenuItem.Checked Then
            settings.DarkMode = True

            ' Disable the DarkModeEnableToolStripMenuItem so that it does not get unchecked when clicked again.
            DarkModeEnableToolStripMenuItem.Enabled = False

            ' Enable the DarkModeDisableToolStripMenuItem so that it can be checked to disable dark mode.
            DarkModeDisableToolStripMenuItem.Enabled = True
            DarkModeDisableToolStripMenuItem.Checked = False

            ' Save the new setting and apply it
            settings.ToggleSettings(True, "darkmode")
        End If
    End Sub

    ''' <summary>
    ''' Handles the CheckedChanged event of DarkModeDisableToolStripMenuItem.
    ''' If DarkModeDisableToolStripMenuItem is checked, DarkMode is disabled,
    ''' DarkModeEnableToolStripMenuItem is unchecked, and the settings are saved and applied.
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">The EventArgs instance containing the event data.</param>
    Private Sub DarkModeDisableToolStripMenuItem_CheckedChanged(sender As Object, e As EventArgs) Handles DarkModeDisableToolStripMenuItem.CheckedChanged
        If DarkModeDisableToolStripMenuItem.Checked Then
            settings.DarkMode = False

            ' Disable the DarkModeDisableToolStripMenuItem so that it does not get unchecked when clicked again.
            DarkModeDisableToolStripMenuItem.Enabled = False

            ' Enable the DarkModeEnableToolStripMenuItem so that it can be checked to enabled dark mode.
            DarkModeEnableToolStripMenuItem.Enabled = True
            DarkModeEnableToolStripMenuItem.Checked = False

            ' Save the new setting and apply it
            settings.ToggleSettings(False, "darkmode")
        End If
    End Sub
End Class
