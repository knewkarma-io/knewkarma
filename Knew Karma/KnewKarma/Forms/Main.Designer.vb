﻿<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()>
Partial Class Main
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()>
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()>
    Private Sub InitializeComponent()
        components = New ComponentModel.Container()
        Dim resources As ComponentModel.ComponentResourceManager = New ComponentModel.ComponentResourceManager(GetType(Main))
        Dim TreeNode1 As TreeNode = New TreeNode("Subreddit")
        Dim TreeNode2 As TreeNode = New TreeNode("User")
        Dim TreeNode3 As TreeNode = New TreeNode("Front Page")
        Dim TreeNode4 As TreeNode = New TreeNode("Listings")
        Dim TreeNode5 As TreeNode = New TreeNode("Post (N/A)")
        Dim TreeNode6 As TreeNode = New TreeNode("Search")
        Dim TreeNode7 As TreeNode = New TreeNode("Posts", New TreeNode() {TreeNode3, TreeNode4, TreeNode5, TreeNode6})
        Dim TreeNode8 As TreeNode = New TreeNode("Username", New TreeNode() {TreeNode1, TreeNode2, TreeNode7})
        TextBoxQuery = New TextBox()
        ButtonSearch = New Button()
        ContextMenuStripRightClick = New ContextMenuStrip(components)
        AboutToolStripMenuItem = New ToolStripMenuItem()
        SettingsToolStripMenuItem = New ToolStripMenuItem()
        DarkModeToolStripMenuItem = New ToolStripMenuItem()
        DarkModeEnableToolStripMenuItem = New ToolStripMenuItem()
        DarkModeDisableToolStripMenuItem = New ToolStripMenuItem()
        SaveDataToolStripMenuItem = New ToolStripMenuItem()
        ToJSONToolStripMenuItem = New ToolStripMenuItem()
        ToCSVToolStripMenuItem = New ToolStripMenuItem()
        ExitToolStripMenuItem = New ToolStripMenuItem()
        TextBoxUsername = New TextBox()
        TextBoxSubreddit = New TextBox()
        RadioButtonUserComments = New RadioButton()
        RadioButtonUserPosts = New RadioButton()
        RadioButtonUserProfile = New RadioButton()
        RadioButtonSubredditProfile = New RadioButton()
        RadioButtonSubredditPosts = New RadioButton()
        ComboBoxUserPostsListing = New ComboBox()
        ComboBoxSearchResultListing = New ComboBox()
        ComboBoxSubredditPostsListing = New ComboBox()
        ComboBoxFrontPageDataListing = New ComboBox()
        RadioButtonBest = New RadioButton()
        RadioButtonPopular = New RadioButton()
        RadioButtonRising = New RadioButton()
        RadioButtonControversial = New RadioButton()
        ComboBoxPostListingsListing = New ComboBox()
        GroupBoxSearchResultsFiltering = New GroupBox()
        LabelSearchResultsLimit = New Label()
        LabelSearchResultsListing = New Label()
        NumericUpDownSearchResultLimit = New NumericUpDown()
        GroupBoxFrontPageDataFiltering = New GroupBox()
        LabelFrontPageDataLimit = New Label()
        LabelFrontPageDataListing = New Label()
        NumericUpDownFrontPageDataLimit = New NumericUpDown()
        ButtonFetchFrontPageData = New Button()
        GroupBoxSubredditDataFiltering = New GroupBox()
        LabelSubredditDataLimit = New Label()
        LabelSubredditPostsListing = New Label()
        NumericUpDownSubredditDataLimit = New NumericUpDown()
        ButtonFetchSubredditData = New Button()
        GroupBoxSubredditData = New GroupBox()
        GroupBoxUserDataFiltering = New GroupBox()
        LabelUserDataLimit = New Label()
        LabelUserPostsListing = New Label()
        NumericUpDownUserDataLimit = New NumericUpDown()
        ButtonFetchUserData = New Button()
        GroupBoxUserData = New GroupBox()
        TreeView1 = New TreeView()
        PanelUserData = New Panel()
        PanelUserDataHeader = New Panel()
        Label1 = New Label()
        PanelSubredditData = New Panel()
        PanelSubredditDataHeader = New Panel()
        Label2 = New Label()
        PanelFrontPageData = New Panel()
        PanelFrontPageHeader = New Panel()
        Label5 = New Label()
        PanelPostListings = New Panel()
        ButtonFetchPostListings = New Button()
        PanelPostListingsDataHeader = New Panel()
        Label3 = New Label()
        GroupBoxPostListingsFiltering = New GroupBox()
        LabelPostListingsListing = New Label()
        LabelPostListingsLimit = New Label()
        NumericUpDownPostListingsLimit = New NumericUpDown()
        GroupBoxPostListings = New GroupBox()
        PanelSearchPosts = New Panel()
        Panel1 = New Panel()
        Label4 = New Label()
        NotifyIcon1 = New NotifyIcon(components)
        PanelPostData = New Panel()
        TextBoxPostSubreddit = New TextBox()
        ButtonFetchPostData = New Button()
        PanelPostDataHeader = New Panel()
        Label6 = New Label()
        TextBoxPostID = New TextBox()
        GroupBoxPostDataFiltering = New GroupBox()
        Label7 = New Label()
        Label8 = New Label()
        NumericUpDownPostDataLimit = New NumericUpDown()
        ComboBoxPostDataListing = New ComboBox()
        GroupBoxPostData = New GroupBox()
        RadioButtonPostProfile = New RadioButton()
        RadioButtonPostComments = New RadioButton()
        ContextMenuStripRightClick.SuspendLayout()
        GroupBoxSearchResultsFiltering.SuspendLayout()
        CType(NumericUpDownSearchResultLimit, ComponentModel.ISupportInitialize).BeginInit()
        GroupBoxFrontPageDataFiltering.SuspendLayout()
        CType(NumericUpDownFrontPageDataLimit, ComponentModel.ISupportInitialize).BeginInit()
        GroupBoxSubredditDataFiltering.SuspendLayout()
        CType(NumericUpDownSubredditDataLimit, ComponentModel.ISupportInitialize).BeginInit()
        GroupBoxSubredditData.SuspendLayout()
        GroupBoxUserDataFiltering.SuspendLayout()
        CType(NumericUpDownUserDataLimit, ComponentModel.ISupportInitialize).BeginInit()
        GroupBoxUserData.SuspendLayout()
        PanelUserData.SuspendLayout()
        PanelUserDataHeader.SuspendLayout()
        PanelSubredditData.SuspendLayout()
        PanelSubredditDataHeader.SuspendLayout()
        PanelFrontPageData.SuspendLayout()
        PanelFrontPageHeader.SuspendLayout()
        PanelPostListings.SuspendLayout()
        PanelPostListingsDataHeader.SuspendLayout()
        GroupBoxPostListingsFiltering.SuspendLayout()
        CType(NumericUpDownPostListingsLimit, ComponentModel.ISupportInitialize).BeginInit()
        GroupBoxPostListings.SuspendLayout()
        PanelSearchPosts.SuspendLayout()
        Panel1.SuspendLayout()
        PanelPostData.SuspendLayout()
        PanelPostDataHeader.SuspendLayout()
        GroupBoxPostDataFiltering.SuspendLayout()
        CType(NumericUpDownPostDataLimit, ComponentModel.ISupportInitialize).BeginInit()
        GroupBoxPostData.SuspendLayout()
        SuspendLayout()
        ' 
        ' TextBoxQuery
        ' 
        TextBoxQuery.BackColor = SystemColors.Window
        TextBoxQuery.Font = New Font("Segoe UI Variable Display Semib", 9F, FontStyle.Bold, GraphicsUnit.Point)
        TextBoxQuery.ForeColor = SystemColors.WindowText
        TextBoxQuery.Location = New Point(3, 103)
        TextBoxQuery.Name = "TextBoxQuery"
        TextBoxQuery.PlaceholderText = "Search query (e.g., osint)"
        TextBoxQuery.Size = New Size(131, 23)
        TextBoxQuery.TabIndex = 0
        ' 
        ' ButtonSearch
        ' 
        ButtonSearch.FlatStyle = FlatStyle.Popup
        ButtonSearch.Font = New Font("Segoe UI Variable Display", 9F, FontStyle.Regular, GraphicsUnit.Point)
        ButtonSearch.ForeColor = Color.Black
        ButtonSearch.Location = New Point(140, 103)
        ButtonSearch.Name = "ButtonSearch"
        ButtonSearch.Size = New Size(79, 24)
        ButtonSearch.TabIndex = 6
        ButtonSearch.Text = "&Search"
        ButtonSearch.UseVisualStyleBackColor = True
        ' 
        ' ContextMenuStripRightClick
        ' 
        ContextMenuStripRightClick.Font = New Font("Segoe UI Variable Text", 9F, FontStyle.Regular, GraphicsUnit.Point)
        ContextMenuStripRightClick.Items.AddRange(New ToolStripItem() {AboutToolStripMenuItem, SettingsToolStripMenuItem, ExitToolStripMenuItem})
        ContextMenuStripRightClick.LayoutStyle = ToolStripLayoutStyle.Table
        ContextMenuStripRightClick.Name = "ContextMenuStrip1"
        ContextMenuStripRightClick.Size = New Size(118, 70)
        ContextMenuStripRightClick.Text = "Menu"
        ' 
        ' AboutToolStripMenuItem
        ' 
        AboutToolStripMenuItem.AutoToolTip = True
        AboutToolStripMenuItem.Font = New Font("Segoe UI Variable Display", 9F, FontStyle.Regular, GraphicsUnit.Point)
        AboutToolStripMenuItem.Image = CType(resources.GetObject("AboutToolStripMenuItem.Image"), Image)
        AboutToolStripMenuItem.Name = "AboutToolStripMenuItem"
        AboutToolStripMenuItem.Size = New Size(117, 22)
        AboutToolStripMenuItem.Text = "About"
        ' 
        ' SettingsToolStripMenuItem
        ' 
        SettingsToolStripMenuItem.AutoToolTip = True
        SettingsToolStripMenuItem.DropDownItems.AddRange(New ToolStripItem() {DarkModeToolStripMenuItem, SaveDataToolStripMenuItem})
        SettingsToolStripMenuItem.Font = New Font("Segoe UI Variable Display", 9F, FontStyle.Regular, GraphicsUnit.Point)
        SettingsToolStripMenuItem.Image = CType(resources.GetObject("SettingsToolStripMenuItem.Image"), Image)
        SettingsToolStripMenuItem.Name = "SettingsToolStripMenuItem"
        SettingsToolStripMenuItem.Size = New Size(117, 22)
        SettingsToolStripMenuItem.Text = "Settings"
        ' 
        ' DarkModeToolStripMenuItem
        ' 
        DarkModeToolStripMenuItem.AutoToolTip = True
        DarkModeToolStripMenuItem.DropDownItems.AddRange(New ToolStripItem() {DarkModeEnableToolStripMenuItem, DarkModeDisableToolStripMenuItem})
        DarkModeToolStripMenuItem.Font = New Font("Segoe UI Variable Display", 9F, FontStyle.Regular, GraphicsUnit.Point)
        DarkModeToolStripMenuItem.Image = CType(resources.GetObject("DarkModeToolStripMenuItem.Image"), Image)
        DarkModeToolStripMenuItem.Name = "DarkModeToolStripMenuItem"
        DarkModeToolStripMenuItem.Size = New Size(135, 22)
        DarkModeToolStripMenuItem.Text = "Dark Mode"
        ' 
        ' DarkModeEnableToolStripMenuItem
        ' 
        DarkModeEnableToolStripMenuItem.AutoToolTip = True
        DarkModeEnableToolStripMenuItem.CheckOnClick = True
        DarkModeEnableToolStripMenuItem.Image = CType(resources.GetObject("DarkModeEnableToolStripMenuItem.Image"), Image)
        DarkModeEnableToolStripMenuItem.Name = "DarkModeEnableToolStripMenuItem"
        DarkModeEnableToolStripMenuItem.Size = New Size(112, 22)
        DarkModeEnableToolStripMenuItem.Text = "Enable"
        ' 
        ' DarkModeDisableToolStripMenuItem
        ' 
        DarkModeDisableToolStripMenuItem.AutoToolTip = True
        DarkModeDisableToolStripMenuItem.CheckOnClick = True
        DarkModeDisableToolStripMenuItem.Image = CType(resources.GetObject("DarkModeDisableToolStripMenuItem.Image"), Image)
        DarkModeDisableToolStripMenuItem.Name = "DarkModeDisableToolStripMenuItem"
        DarkModeDisableToolStripMenuItem.Size = New Size(112, 22)
        DarkModeDisableToolStripMenuItem.Text = "Disable"
        ' 
        ' SaveDataToolStripMenuItem
        ' 
        SaveDataToolStripMenuItem.AutoToolTip = True
        SaveDataToolStripMenuItem.DropDownItems.AddRange(New ToolStripItem() {ToJSONToolStripMenuItem, ToCSVToolStripMenuItem})
        SaveDataToolStripMenuItem.Image = CType(resources.GetObject("SaveDataToolStripMenuItem.Image"), Image)
        SaveDataToolStripMenuItem.Name = "SaveDataToolStripMenuItem"
        SaveDataToolStripMenuItem.Size = New Size(135, 22)
        SaveDataToolStripMenuItem.Text = "Save Data..."
        ' 
        ' ToJSONToolStripMenuItem
        ' 
        ToJSONToolStripMenuItem.AutoToolTip = True
        ToJSONToolStripMenuItem.CheckOnClick = True
        ToJSONToolStripMenuItem.Image = CType(resources.GetObject("ToJSONToolStripMenuItem.Image"), Image)
        ToJSONToolStripMenuItem.Name = "ToJSONToolStripMenuItem"
        ToJSONToolStripMenuItem.Size = New Size(118, 22)
        ToJSONToolStripMenuItem.Text = "to JSON"
        ' 
        ' ToCSVToolStripMenuItem
        ' 
        ToCSVToolStripMenuItem.AutoToolTip = True
        ToCSVToolStripMenuItem.CheckOnClick = True
        ToCSVToolStripMenuItem.Image = CType(resources.GetObject("ToCSVToolStripMenuItem.Image"), Image)
        ToCSVToolStripMenuItem.Name = "ToCSVToolStripMenuItem"
        ToCSVToolStripMenuItem.Size = New Size(118, 22)
        ToCSVToolStripMenuItem.Text = "to CSV"
        ' 
        ' ExitToolStripMenuItem
        ' 
        ExitToolStripMenuItem.AutoToolTip = True
        ExitToolStripMenuItem.Font = New Font("Segoe UI Variable Display Semib", 9F, FontStyle.Bold, GraphicsUnit.Point)
        ExitToolStripMenuItem.Image = CType(resources.GetObject("ExitToolStripMenuItem.Image"), Image)
        ExitToolStripMenuItem.Name = "ExitToolStripMenuItem"
        ExitToolStripMenuItem.Size = New Size(117, 22)
        ExitToolStripMenuItem.Text = "&Exit"
        ' 
        ' TextBoxUsername
        ' 
        TextBoxUsername.BackColor = SystemColors.Window
        TextBoxUsername.Font = New Font("Segoe UI Variable Display Semib", 9F, FontStyle.Bold, GraphicsUnit.Point)
        TextBoxUsername.ForeColor = SystemColors.WindowText
        TextBoxUsername.Location = New Point(3, 162)
        TextBoxUsername.Name = "TextBoxUsername"
        TextBoxUsername.PlaceholderText = "Username (e.g., JohnDoe)"
        TextBoxUsername.Size = New Size(131, 23)
        TextBoxUsername.TabIndex = 1
        ' 
        ' TextBoxSubreddit
        ' 
        TextBoxSubreddit.Font = New Font("Segoe UI Variable Display Semib", 9F, FontStyle.Bold, GraphicsUnit.Point)
        TextBoxSubreddit.Location = New Point(3, 162)
        TextBoxSubreddit.Name = "TextBoxSubreddit"
        TextBoxSubreddit.PlaceholderText = "Subreddit (e.g., Ask)"
        TextBoxSubreddit.Size = New Size(131, 23)
        TextBoxSubreddit.TabIndex = 5
        ' 
        ' RadioButtonUserComments
        ' 
        RadioButtonUserComments.AutoSize = True
        RadioButtonUserComments.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        RadioButtonUserComments.Location = New Point(130, 23)
        RadioButtonUserComments.Name = "RadioButtonUserComments"
        RadioButtonUserComments.Size = New Size(80, 19)
        RadioButtonUserComments.TabIndex = 7
        RadioButtonUserComments.Text = " Comments"
        RadioButtonUserComments.UseVisualStyleBackColor = True
        ' 
        ' RadioButtonUserPosts
        ' 
        RadioButtonUserPosts.AutoSize = True
        RadioButtonUserPosts.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        RadioButtonUserPosts.Location = New Point(71, 23)
        RadioButtonUserPosts.Name = "RadioButtonUserPosts"
        RadioButtonUserPosts.Size = New Size(51, 19)
        RadioButtonUserPosts.TabIndex = 6
        RadioButtonUserPosts.Text = "Posts"
        RadioButtonUserPosts.UseVisualStyleBackColor = True
        ' 
        ' RadioButtonUserProfile
        ' 
        RadioButtonUserProfile.AutoSize = True
        RadioButtonUserProfile.Checked = True
        RadioButtonUserProfile.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        RadioButtonUserProfile.Location = New Point(6, 23)
        RadioButtonUserProfile.Name = "RadioButtonUserProfile"
        RadioButtonUserProfile.Size = New Size(56, 19)
        RadioButtonUserProfile.TabIndex = 5
        RadioButtonUserProfile.TabStop = True
        RadioButtonUserProfile.Text = "Profile"
        RadioButtonUserProfile.UseVisualStyleBackColor = True
        ' 
        ' RadioButtonSubredditProfile
        ' 
        RadioButtonSubredditProfile.AutoSize = True
        RadioButtonSubredditProfile.Checked = True
        RadioButtonSubredditProfile.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        RadioButtonSubredditProfile.Location = New Point(6, 23)
        RadioButtonSubredditProfile.Name = "RadioButtonSubredditProfile"
        RadioButtonSubredditProfile.Size = New Size(56, 19)
        RadioButtonSubredditProfile.TabIndex = 5
        RadioButtonSubredditProfile.TabStop = True
        RadioButtonSubredditProfile.Text = "Profile"
        RadioButtonSubredditProfile.UseVisualStyleBackColor = True
        ' 
        ' RadioButtonSubredditPosts
        ' 
        RadioButtonSubredditPosts.AutoSize = True
        RadioButtonSubredditPosts.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        RadioButtonSubredditPosts.Location = New Point(71, 23)
        RadioButtonSubredditPosts.Name = "RadioButtonSubredditPosts"
        RadioButtonSubredditPosts.Size = New Size(51, 19)
        RadioButtonSubredditPosts.TabIndex = 6
        RadioButtonSubredditPosts.Text = "Posts"
        RadioButtonSubredditPosts.UseVisualStyleBackColor = True
        ' 
        ' ComboBoxUserPostsListing
        ' 
        ComboBoxUserPostsListing.AutoCompleteCustomSource.AddRange(New String() {"Controversial", "Hot", "Best", "New", "Rising"})
        ComboBoxUserPostsListing.AutoCompleteSource = AutoCompleteSource.CustomSource
        ComboBoxUserPostsListing.BackColor = SystemColors.Window
        ComboBoxUserPostsListing.DropDownStyle = ComboBoxStyle.DropDownList
        ComboBoxUserPostsListing.Enabled = False
        ComboBoxUserPostsListing.FlatStyle = FlatStyle.Popup
        ComboBoxUserPostsListing.Font = New Font("Segoe UI Variable Display Semib", 8.25F, FontStyle.Bold, GraphicsUnit.Point)
        ComboBoxUserPostsListing.ForeColor = SystemColors.WindowText
        ComboBoxUserPostsListing.FormattingEnabled = True
        ComboBoxUserPostsListing.Items.AddRange(New Object() {"all", "best", "controversial", "hot", "new", "rising", "top"})
        ComboBoxUserPostsListing.Location = New Point(6, 40)
        ComboBoxUserPostsListing.Name = "ComboBoxUserPostsListing"
        ComboBoxUserPostsListing.Size = New Size(116, 23)
        ComboBoxUserPostsListing.Sorted = True
        ComboBoxUserPostsListing.TabIndex = 11
        ' 
        ' ComboBoxSearchResultListing
        ' 
        ComboBoxSearchResultListing.AutoCompleteCustomSource.AddRange(New String() {"Controversial", "Hot", "Best", "New", "Rising"})
        ComboBoxSearchResultListing.AutoCompleteSource = AutoCompleteSource.CustomSource
        ComboBoxSearchResultListing.BackColor = SystemColors.Window
        ComboBoxSearchResultListing.DropDownStyle = ComboBoxStyle.DropDownList
        ComboBoxSearchResultListing.FlatStyle = FlatStyle.Popup
        ComboBoxSearchResultListing.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        ComboBoxSearchResultListing.ForeColor = SystemColors.WindowText
        ComboBoxSearchResultListing.FormattingEnabled = True
        ComboBoxSearchResultListing.Items.AddRange(New Object() {"all", "best", "controversial", "hot", "new", "rising", "top"})
        ComboBoxSearchResultListing.Location = New Point(6, 40)
        ComboBoxSearchResultListing.Name = "ComboBoxSearchResultListing"
        ComboBoxSearchResultListing.Size = New Size(116, 23)
        ComboBoxSearchResultListing.Sorted = True
        ComboBoxSearchResultListing.TabIndex = 11
        ' 
        ' ComboBoxSubredditPostsListing
        ' 
        ComboBoxSubredditPostsListing.AutoCompleteCustomSource.AddRange(New String() {"Controversial", "Hot", "Best", "New", "Rising"})
        ComboBoxSubredditPostsListing.AutoCompleteSource = AutoCompleteSource.CustomSource
        ComboBoxSubredditPostsListing.BackColor = SystemColors.Window
        ComboBoxSubredditPostsListing.DropDownStyle = ComboBoxStyle.DropDownList
        ComboBoxSubredditPostsListing.Enabled = False
        ComboBoxSubredditPostsListing.FlatStyle = FlatStyle.Popup
        ComboBoxSubredditPostsListing.Font = New Font("Segoe UI Variable Display Semib", 8.25F, FontStyle.Bold, GraphicsUnit.Point)
        ComboBoxSubredditPostsListing.ForeColor = SystemColors.WindowText
        ComboBoxSubredditPostsListing.FormattingEnabled = True
        ComboBoxSubredditPostsListing.Items.AddRange(New Object() {"all", "best", "controversial", "hot", "new", "rising", "top"})
        ComboBoxSubredditPostsListing.Location = New Point(6, 40)
        ComboBoxSubredditPostsListing.Name = "ComboBoxSubredditPostsListing"
        ComboBoxSubredditPostsListing.Size = New Size(116, 23)
        ComboBoxSubredditPostsListing.Sorted = True
        ComboBoxSubredditPostsListing.TabIndex = 11
        ' 
        ' ComboBoxFrontPageDataListing
        ' 
        ComboBoxFrontPageDataListing.AutoCompleteCustomSource.AddRange(New String() {"Controversial", "Hot", "Best", "New", "Rising"})
        ComboBoxFrontPageDataListing.AutoCompleteSource = AutoCompleteSource.CustomSource
        ComboBoxFrontPageDataListing.BackColor = SystemColors.Window
        ComboBoxFrontPageDataListing.DropDownStyle = ComboBoxStyle.DropDownList
        ComboBoxFrontPageDataListing.FlatStyle = FlatStyle.Popup
        ComboBoxFrontPageDataListing.Font = New Font("Segoe UI Variable Display Semib", 8.25F, FontStyle.Bold, GraphicsUnit.Point)
        ComboBoxFrontPageDataListing.ForeColor = SystemColors.WindowText
        ComboBoxFrontPageDataListing.FormattingEnabled = True
        ComboBoxFrontPageDataListing.Items.AddRange(New Object() {"all", "best", "controversial", "hot", "new", "rising", "top"})
        ComboBoxFrontPageDataListing.Location = New Point(6, 40)
        ComboBoxFrontPageDataListing.Name = "ComboBoxFrontPageDataListing"
        ComboBoxFrontPageDataListing.Size = New Size(116, 23)
        ComboBoxFrontPageDataListing.Sorted = True
        ComboBoxFrontPageDataListing.TabIndex = 11
        ' 
        ' RadioButtonBest
        ' 
        RadioButtonBest.AutoSize = True
        RadioButtonBest.Checked = True
        RadioButtonBest.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        RadioButtonBest.Location = New Point(6, 23)
        RadioButtonBest.Name = "RadioButtonBest"
        RadioButtonBest.Size = New Size(46, 19)
        RadioButtonBest.TabIndex = 5
        RadioButtonBest.TabStop = True
        RadioButtonBest.Text = "Best"
        RadioButtonBest.UseVisualStyleBackColor = True
        ' 
        ' RadioButtonPopular
        ' 
        RadioButtonPopular.AutoSize = True
        RadioButtonPopular.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        RadioButtonPopular.Location = New Point(6, 44)
        RadioButtonPopular.Name = "RadioButtonPopular"
        RadioButtonPopular.Size = New Size(62, 19)
        RadioButtonPopular.TabIndex = 7
        RadioButtonPopular.Text = "Popular"
        RadioButtonPopular.UseVisualStyleBackColor = True
        ' 
        ' RadioButtonRising
        ' 
        RadioButtonRising.AutoSize = True
        RadioButtonRising.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        RadioButtonRising.Location = New Point(58, 23)
        RadioButtonRising.Name = "RadioButtonRising"
        RadioButtonRising.Size = New Size(55, 19)
        RadioButtonRising.TabIndex = 6
        RadioButtonRising.Text = "Rising"
        RadioButtonRising.UseVisualStyleBackColor = True
        ' 
        ' RadioButtonControversial
        ' 
        RadioButtonControversial.AutoSize = True
        RadioButtonControversial.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        RadioButtonControversial.Location = New Point(119, 23)
        RadioButtonControversial.Name = "RadioButtonControversial"
        RadioButtonControversial.Size = New Size(90, 19)
        RadioButtonControversial.TabIndex = 8
        RadioButtonControversial.Text = "Controversial"
        RadioButtonControversial.UseVisualStyleBackColor = True
        ' 
        ' ComboBoxPostListingsListing
        ' 
        ComboBoxPostListingsListing.AutoCompleteCustomSource.AddRange(New String() {"Controversial", "Hot", "Best", "New", "Rising"})
        ComboBoxPostListingsListing.AutoCompleteSource = AutoCompleteSource.CustomSource
        ComboBoxPostListingsListing.BackColor = SystemColors.Window
        ComboBoxPostListingsListing.DropDownStyle = ComboBoxStyle.DropDownList
        ComboBoxPostListingsListing.FlatStyle = FlatStyle.Popup
        ComboBoxPostListingsListing.Font = New Font("Segoe UI Variable Display Semib", 8.25F, FontStyle.Bold, GraphicsUnit.Point)
        ComboBoxPostListingsListing.ForeColor = SystemColors.WindowText
        ComboBoxPostListingsListing.FormattingEnabled = True
        ComboBoxPostListingsListing.Items.AddRange(New Object() {"all", "hot", "new", "top"})
        ComboBoxPostListingsListing.Location = New Point(6, 40)
        ComboBoxPostListingsListing.Name = "ComboBoxPostListingsListing"
        ComboBoxPostListingsListing.Size = New Size(116, 23)
        ComboBoxPostListingsListing.Sorted = True
        ComboBoxPostListingsListing.TabIndex = 11
        ' 
        ' GroupBoxSearchResultsFiltering
        ' 
        GroupBoxSearchResultsFiltering.Controls.Add(LabelSearchResultsLimit)
        GroupBoxSearchResultsFiltering.Controls.Add(LabelSearchResultsListing)
        GroupBoxSearchResultsFiltering.Controls.Add(NumericUpDownSearchResultLimit)
        GroupBoxSearchResultsFiltering.Controls.Add(ComboBoxSearchResultListing)
        GroupBoxSearchResultsFiltering.Font = New Font("Segoe UI Variable Display", 8.25F, FontStyle.Underline, GraphicsUnit.Point)
        GroupBoxSearchResultsFiltering.Location = New Point(3, 23)
        GroupBoxSearchResultsFiltering.Name = "GroupBoxSearchResultsFiltering"
        GroupBoxSearchResultsFiltering.Size = New Size(215, 70)
        GroupBoxSearchResultsFiltering.TabIndex = 11
        GroupBoxSearchResultsFiltering.TabStop = False
        GroupBoxSearchResultsFiltering.Text = "Set posts sort criterion and results limit"
        ' 
        ' LabelSearchResultsLimit
        ' 
        LabelSearchResultsLimit.AutoSize = True
        LabelSearchResultsLimit.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        LabelSearchResultsLimit.Location = New Point(126, 23)
        LabelSearchResultsLimit.Name = "LabelSearchResultsLimit"
        LabelSearchResultsLimit.Size = New Size(82, 15)
        LabelSearchResultsLimit.TabIndex = 19
        LabelSearchResultsLimit.Text = "Limit results to:"
        ' 
        ' LabelSearchResultsListing
        ' 
        LabelSearchResultsListing.AutoSize = True
        LabelSearchResultsListing.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        LabelSearchResultsListing.Location = New Point(4, 22)
        LabelSearchResultsListing.Name = "LabelSearchResultsListing"
        LabelSearchResultsListing.Size = New Size(79, 15)
        LabelSearchResultsListing.TabIndex = 18
        LabelSearchResultsListing.Text = "Sort results by:"
        ' 
        ' NumericUpDownSearchResultLimit
        ' 
        NumericUpDownSearchResultLimit.Font = New Font("Segoe UI Variable Display Semib", 8.25F, FontStyle.Bold, GraphicsUnit.Point)
        NumericUpDownSearchResultLimit.Location = New Point(130, 41)
        NumericUpDownSearchResultLimit.Minimum = New Decimal(New Integer() {5, 0, 0, 0})
        NumericUpDownSearchResultLimit.Name = "NumericUpDownSearchResultLimit"
        NumericUpDownSearchResultLimit.ReadOnly = True
        NumericUpDownSearchResultLimit.Size = New Size(79, 22)
        NumericUpDownSearchResultLimit.TabIndex = 17
        NumericUpDownSearchResultLimit.Value = New Decimal(New Integer() {10, 0, 0, 0})
        ' 
        ' GroupBoxFrontPageDataFiltering
        ' 
        GroupBoxFrontPageDataFiltering.Controls.Add(LabelFrontPageDataLimit)
        GroupBoxFrontPageDataFiltering.Controls.Add(LabelFrontPageDataListing)
        GroupBoxFrontPageDataFiltering.Controls.Add(NumericUpDownFrontPageDataLimit)
        GroupBoxFrontPageDataFiltering.Controls.Add(ComboBoxFrontPageDataListing)
        GroupBoxFrontPageDataFiltering.Font = New Font("Segoe UI Variable Display", 8.25F, FontStyle.Underline, GraphicsUnit.Point)
        GroupBoxFrontPageDataFiltering.Location = New Point(3, 23)
        GroupBoxFrontPageDataFiltering.Name = "GroupBoxFrontPageDataFiltering"
        GroupBoxFrontPageDataFiltering.Size = New Size(215, 70)
        GroupBoxFrontPageDataFiltering.TabIndex = 19
        GroupBoxFrontPageDataFiltering.TabStop = False
        GroupBoxFrontPageDataFiltering.Text = "Set posts sort criterion and output limit"
        ' 
        ' LabelFrontPageDataLimit
        ' 
        LabelFrontPageDataLimit.AutoSize = True
        LabelFrontPageDataLimit.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        LabelFrontPageDataLimit.Location = New Point(126, 23)
        LabelFrontPageDataLimit.Name = "LabelFrontPageDataLimit"
        LabelFrontPageDataLimit.Size = New Size(81, 15)
        LabelFrontPageDataLimit.TabIndex = 19
        LabelFrontPageDataLimit.Text = "Limit output to:"
        ' 
        ' LabelFrontPageDataListing
        ' 
        LabelFrontPageDataListing.AutoSize = True
        LabelFrontPageDataListing.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        LabelFrontPageDataListing.Location = New Point(4, 22)
        LabelFrontPageDataListing.Name = "LabelFrontPageDataListing"
        LabelFrontPageDataListing.Size = New Size(72, 15)
        LabelFrontPageDataListing.TabIndex = 18
        LabelFrontPageDataListing.Text = "Sort posts by:"
        ' 
        ' NumericUpDownFrontPageDataLimit
        ' 
        NumericUpDownFrontPageDataLimit.Font = New Font("Segoe UI Variable Text Semibold", 8.25F, FontStyle.Bold, GraphicsUnit.Point)
        NumericUpDownFrontPageDataLimit.Location = New Point(130, 41)
        NumericUpDownFrontPageDataLimit.Minimum = New Decimal(New Integer() {5, 0, 0, 0})
        NumericUpDownFrontPageDataLimit.Name = "NumericUpDownFrontPageDataLimit"
        NumericUpDownFrontPageDataLimit.ReadOnly = True
        NumericUpDownFrontPageDataLimit.Size = New Size(79, 22)
        NumericUpDownFrontPageDataLimit.TabIndex = 17
        NumericUpDownFrontPageDataLimit.Value = New Decimal(New Integer() {10, 0, 0, 0})
        ' 
        ' ButtonFetchFrontPageData
        ' 
        ButtonFetchFrontPageData.FlatStyle = FlatStyle.Popup
        ButtonFetchFrontPageData.Font = New Font("Segoe UI Variable Display", 9F, FontStyle.Regular, GraphicsUnit.Point)
        ButtonFetchFrontPageData.ForeColor = Color.Black
        ButtonFetchFrontPageData.Location = New Point(139, 103)
        ButtonFetchFrontPageData.Name = "ButtonFetchFrontPageData"
        ButtonFetchFrontPageData.Size = New Size(79, 24)
        ButtonFetchFrontPageData.TabIndex = 17
        ButtonFetchFrontPageData.Text = "&Fetch"
        ButtonFetchFrontPageData.UseVisualStyleBackColor = True
        ' 
        ' GroupBoxSubredditDataFiltering
        ' 
        GroupBoxSubredditDataFiltering.Controls.Add(LabelSubredditDataLimit)
        GroupBoxSubredditDataFiltering.Controls.Add(LabelSubredditPostsListing)
        GroupBoxSubredditDataFiltering.Controls.Add(NumericUpDownSubredditDataLimit)
        GroupBoxSubredditDataFiltering.Controls.Add(ComboBoxSubredditPostsListing)
        GroupBoxSubredditDataFiltering.Font = New Font("Segoe UI Variable Display", 8.25F, FontStyle.Underline, GraphicsUnit.Point)
        GroupBoxSubredditDataFiltering.Location = New Point(3, 81)
        GroupBoxSubredditDataFiltering.Name = "GroupBoxSubredditDataFiltering"
        GroupBoxSubredditDataFiltering.Size = New Size(215, 70)
        GroupBoxSubredditDataFiltering.TabIndex = 11
        GroupBoxSubredditDataFiltering.TabStop = False
        GroupBoxSubredditDataFiltering.Text = "Set posts sort criterion and output limit"
        ' 
        ' LabelSubredditDataLimit
        ' 
        LabelSubredditDataLimit.AutoSize = True
        LabelSubredditDataLimit.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        LabelSubredditDataLimit.Location = New Point(126, 23)
        LabelSubredditDataLimit.Name = "LabelSubredditDataLimit"
        LabelSubredditDataLimit.Size = New Size(81, 15)
        LabelSubredditDataLimit.TabIndex = 19
        LabelSubredditDataLimit.Text = "Limit output to:"
        ' 
        ' LabelSubredditPostsListing
        ' 
        LabelSubredditPostsListing.AutoSize = True
        LabelSubredditPostsListing.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        LabelSubredditPostsListing.Location = New Point(4, 22)
        LabelSubredditPostsListing.Name = "LabelSubredditPostsListing"
        LabelSubredditPostsListing.Size = New Size(72, 15)
        LabelSubredditPostsListing.TabIndex = 18
        LabelSubredditPostsListing.Text = "Sort posts by:"
        ' 
        ' NumericUpDownSubredditDataLimit
        ' 
        NumericUpDownSubredditDataLimit.Enabled = False
        NumericUpDownSubredditDataLimit.Font = New Font("Segoe UI Variable Display Semib", 8.25F, FontStyle.Bold, GraphicsUnit.Point)
        NumericUpDownSubredditDataLimit.Location = New Point(130, 41)
        NumericUpDownSubredditDataLimit.Minimum = New Decimal(New Integer() {5, 0, 0, 0})
        NumericUpDownSubredditDataLimit.Name = "NumericUpDownSubredditDataLimit"
        NumericUpDownSubredditDataLimit.ReadOnly = True
        NumericUpDownSubredditDataLimit.Size = New Size(79, 22)
        NumericUpDownSubredditDataLimit.TabIndex = 17
        NumericUpDownSubredditDataLimit.Value = New Decimal(New Integer() {10, 0, 0, 0})
        ' 
        ' ButtonFetchSubredditData
        ' 
        ButtonFetchSubredditData.FlatStyle = FlatStyle.Popup
        ButtonFetchSubredditData.Font = New Font("Segoe UI Variable Display", 9F, FontStyle.Regular, GraphicsUnit.Point)
        ButtonFetchSubredditData.ForeColor = Color.Black
        ButtonFetchSubredditData.Location = New Point(140, 162)
        ButtonFetchSubredditData.Name = "ButtonFetchSubredditData"
        ButtonFetchSubredditData.Size = New Size(79, 24)
        ButtonFetchSubredditData.TabIndex = 6
        ButtonFetchSubredditData.Text = "&Fetch"
        ButtonFetchSubredditData.UseVisualStyleBackColor = True
        ' 
        ' GroupBoxSubredditData
        ' 
        GroupBoxSubredditData.BackColor = Color.Transparent
        GroupBoxSubredditData.ContextMenuStrip = ContextMenuStripRightClick
        GroupBoxSubredditData.Controls.Add(RadioButtonSubredditProfile)
        GroupBoxSubredditData.Controls.Add(RadioButtonSubredditPosts)
        GroupBoxSubredditData.FlatStyle = FlatStyle.Flat
        GroupBoxSubredditData.Font = New Font("Segoe UI Variable Display", 8.25F, FontStyle.Underline, GraphicsUnit.Point)
        GroupBoxSubredditData.Location = New Point(3, 26)
        GroupBoxSubredditData.Name = "GroupBoxSubredditData"
        GroupBoxSubredditData.Size = New Size(215, 49)
        GroupBoxSubredditData.TabIndex = 9
        GroupBoxSubredditData.TabStop = False
        GroupBoxSubredditData.Text = "Select subreddit data to fetch"
        ' 
        ' GroupBoxUserDataFiltering
        ' 
        GroupBoxUserDataFiltering.Controls.Add(LabelUserDataLimit)
        GroupBoxUserDataFiltering.Controls.Add(LabelUserPostsListing)
        GroupBoxUserDataFiltering.Controls.Add(NumericUpDownUserDataLimit)
        GroupBoxUserDataFiltering.Controls.Add(ComboBoxUserPostsListing)
        GroupBoxUserDataFiltering.Font = New Font("Segoe UI Variable Display", 8.25F, FontStyle.Underline, GraphicsUnit.Point)
        GroupBoxUserDataFiltering.Location = New Point(3, 81)
        GroupBoxUserDataFiltering.Name = "GroupBoxUserDataFiltering"
        GroupBoxUserDataFiltering.Size = New Size(215, 70)
        GroupBoxUserDataFiltering.TabIndex = 10
        GroupBoxUserDataFiltering.TabStop = False
        GroupBoxUserDataFiltering.Text = "Set sort criterion and output limit"
        ' 
        ' LabelUserDataLimit
        ' 
        LabelUserDataLimit.AutoSize = True
        LabelUserDataLimit.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        LabelUserDataLimit.Location = New Point(126, 23)
        LabelUserDataLimit.Name = "LabelUserDataLimit"
        LabelUserDataLimit.Size = New Size(81, 15)
        LabelUserDataLimit.TabIndex = 19
        LabelUserDataLimit.Text = "Limit output to:"
        ' 
        ' LabelUserPostsListing
        ' 
        LabelUserPostsListing.AutoSize = True
        LabelUserPostsListing.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        LabelUserPostsListing.Location = New Point(4, 22)
        LabelUserPostsListing.Name = "LabelUserPostsListing"
        LabelUserPostsListing.Size = New Size(68, 15)
        LabelUserPostsListing.TabIndex = 18
        LabelUserPostsListing.Text = "Sort data by:"
        ' 
        ' NumericUpDownUserDataLimit
        ' 
        NumericUpDownUserDataLimit.Enabled = False
        NumericUpDownUserDataLimit.Font = New Font("Segoe UI Variable Display Semib", 8.25F, FontStyle.Bold, GraphicsUnit.Point)
        NumericUpDownUserDataLimit.Location = New Point(130, 41)
        NumericUpDownUserDataLimit.Minimum = New Decimal(New Integer() {5, 0, 0, 0})
        NumericUpDownUserDataLimit.Name = "NumericUpDownUserDataLimit"
        NumericUpDownUserDataLimit.ReadOnly = True
        NumericUpDownUserDataLimit.Size = New Size(79, 22)
        NumericUpDownUserDataLimit.TabIndex = 17
        NumericUpDownUserDataLimit.Value = New Decimal(New Integer() {10, 0, 0, 0})
        ' 
        ' ButtonFetchUserData
        ' 
        ButtonFetchUserData.FlatStyle = FlatStyle.Popup
        ButtonFetchUserData.Font = New Font("Segoe UI Variable Display", 9F, FontStyle.Regular, GraphicsUnit.Point)
        ButtonFetchUserData.ForeColor = Color.Black
        ButtonFetchUserData.Location = New Point(140, 162)
        ButtonFetchUserData.Name = "ButtonFetchUserData"
        ButtonFetchUserData.Size = New Size(79, 24)
        ButtonFetchUserData.TabIndex = 4
        ButtonFetchUserData.Text = "&Fetch"
        ButtonFetchUserData.UseVisualStyleBackColor = True
        ' 
        ' GroupBoxUserData
        ' 
        GroupBoxUserData.BackColor = Color.Transparent
        GroupBoxUserData.ContextMenuStrip = ContextMenuStripRightClick
        GroupBoxUserData.Controls.Add(RadioButtonUserProfile)
        GroupBoxUserData.Controls.Add(RadioButtonUserComments)
        GroupBoxUserData.Controls.Add(RadioButtonUserPosts)
        GroupBoxUserData.Font = New Font("Segoe UI Variable Display", 8.25F, FontStyle.Underline, GraphicsUnit.Point)
        GroupBoxUserData.Location = New Point(3, 26)
        GroupBoxUserData.Name = "GroupBoxUserData"
        GroupBoxUserData.Size = New Size(215, 49)
        GroupBoxUserData.TabIndex = 8
        GroupBoxUserData.TabStop = False
        GroupBoxUserData.Text = "Select user data to fetch"
        ' 
        ' TreeView1
        ' 
        TreeView1.Location = New Point(12, 12)
        TreeView1.Name = "TreeView1"
        TreeNode1.Name = "childSubreddit"
        TreeNode1.Text = "Subreddit"
        TreeNode2.Name = "childUser"
        TreeNode2.Text = "User"
        TreeNode3.Name = "subchildFrontPage"
        TreeNode3.Text = "Front Page"
        TreeNode4.Name = "subchildListings"
        TreeNode4.Text = "Listings"
        TreeNode5.Name = "childPost"
        TreeNode5.Text = "Post (N/A)"
        TreeNode6.Name = "subchildSearch"
        TreeNode6.Text = "Search"
        TreeNode7.Name = "childPosts"
        TreeNode7.Text = "Posts"
        TreeNode8.Name = "MainRoot"
        TreeNode8.Text = "Username"
        TreeView1.Nodes.AddRange(New TreeNode() {TreeNode8})
        TreeView1.Size = New Size(129, 186)
        TreeView1.TabIndex = 17
        ' 
        ' PanelUserData
        ' 
        PanelUserData.Controls.Add(ButtonFetchUserData)
        PanelUserData.Controls.Add(PanelUserDataHeader)
        PanelUserData.Controls.Add(GroupBoxUserData)
        PanelUserData.Controls.Add(TextBoxUsername)
        PanelUserData.Controls.Add(GroupBoxUserDataFiltering)
        PanelUserData.Location = New Point(147, 12)
        PanelUserData.Name = "PanelUserData"
        PanelUserData.Size = New Size(221, 188)
        PanelUserData.TabIndex = 18
        PanelUserData.Visible = False
        ' 
        ' PanelUserDataHeader
        ' 
        PanelUserDataHeader.BackColor = Color.Transparent
        PanelUserDataHeader.BorderStyle = BorderStyle.FixedSingle
        PanelUserDataHeader.Controls.Add(Label1)
        PanelUserDataHeader.Enabled = False
        PanelUserDataHeader.Location = New Point(3, 0)
        PanelUserDataHeader.Name = "PanelUserDataHeader"
        PanelUserDataHeader.Size = New Size(215, 20)
        PanelUserDataHeader.TabIndex = 29
        ' 
        ' Label1
        ' 
        Label1.AutoSize = True
        Label1.BackColor = Color.Transparent
        Label1.Font = New Font("Segoe UI Variable Display Semib", 9F, FontStyle.Bold, GraphicsUnit.Point)
        Label1.ForeColor = Color.Black
        Label1.Location = New Point(53, 0)
        Label1.Name = "Label1"
        Label1.Size = New Size(108, 16)
        Label1.TabIndex = 29
        Label1.Text = "Fetch a User's data"
        ' 
        ' PanelSubredditData
        ' 
        PanelSubredditData.BackColor = Color.Transparent
        PanelSubredditData.Controls.Add(ButtonFetchSubredditData)
        PanelSubredditData.Controls.Add(PanelSubredditDataHeader)
        PanelSubredditData.Controls.Add(TextBoxSubreddit)
        PanelSubredditData.Controls.Add(GroupBoxSubredditDataFiltering)
        PanelSubredditData.Controls.Add(GroupBoxSubredditData)
        PanelSubredditData.Location = New Point(147, 12)
        PanelSubredditData.Name = "PanelSubredditData"
        PanelSubredditData.Size = New Size(221, 188)
        PanelSubredditData.TabIndex = 21
        PanelSubredditData.Visible = False
        ' 
        ' PanelSubredditDataHeader
        ' 
        PanelSubredditDataHeader.BackColor = Color.Transparent
        PanelSubredditDataHeader.BorderStyle = BorderStyle.FixedSingle
        PanelSubredditDataHeader.Controls.Add(Label2)
        PanelSubredditDataHeader.Enabled = False
        PanelSubredditDataHeader.Location = New Point(3, 0)
        PanelSubredditDataHeader.Name = "PanelSubredditDataHeader"
        PanelSubredditDataHeader.Size = New Size(215, 20)
        PanelSubredditDataHeader.TabIndex = 30
        ' 
        ' Label2
        ' 
        Label2.AutoSize = True
        Label2.BackColor = Color.Transparent
        Label2.Font = New Font("Segoe UI Variable Display Semib", 9F, FontStyle.Bold, GraphicsUnit.Point)
        Label2.ForeColor = Color.Black
        Label2.Location = New Point(34, 0)
        Label2.Name = "Label2"
        Label2.Size = New Size(138, 16)
        Label2.TabIndex = 29
        Label2.Text = "Fetch a Subreddit's data"
        ' 
        ' PanelFrontPageData
        ' 
        PanelFrontPageData.Controls.Add(ButtonFetchFrontPageData)
        PanelFrontPageData.Controls.Add(PanelFrontPageHeader)
        PanelFrontPageData.Controls.Add(GroupBoxFrontPageDataFiltering)
        PanelFrontPageData.Location = New Point(147, 12)
        PanelFrontPageData.Name = "PanelFrontPageData"
        PanelFrontPageData.Size = New Size(221, 188)
        PanelFrontPageData.TabIndex = 25
        PanelFrontPageData.Visible = False
        ' 
        ' PanelFrontPageHeader
        ' 
        PanelFrontPageHeader.BackColor = Color.Transparent
        PanelFrontPageHeader.BorderStyle = BorderStyle.FixedSingle
        PanelFrontPageHeader.Controls.Add(Label5)
        PanelFrontPageHeader.Enabled = False
        PanelFrontPageHeader.Location = New Point(3, 0)
        PanelFrontPageHeader.Name = "PanelFrontPageHeader"
        PanelFrontPageHeader.Size = New Size(215, 20)
        PanelFrontPageHeader.TabIndex = 32
        ' 
        ' Label5
        ' 
        Label5.AutoSize = True
        Label5.BackColor = Color.Transparent
        Label5.Font = New Font("Segoe UI Variable Display Semib", 9F, FontStyle.Bold, GraphicsUnit.Point)
        Label5.ForeColor = Color.Black
        Label5.Location = New Point(7, 0)
        Label5.Name = "Label5"
        Label5.Size = New Size(199, 16)
        Label5.TabIndex = 29
        Label5.Text = "Fetch posts from Reddit Front Page"
        ' 
        ' PanelPostListings
        ' 
        PanelPostListings.Controls.Add(ButtonFetchPostListings)
        PanelPostListings.Controls.Add(PanelPostListingsDataHeader)
        PanelPostListings.Controls.Add(GroupBoxPostListingsFiltering)
        PanelPostListings.Controls.Add(GroupBoxPostListings)
        PanelPostListings.Location = New Point(147, 12)
        PanelPostListings.Name = "PanelPostListings"
        PanelPostListings.Size = New Size(221, 188)
        PanelPostListings.TabIndex = 26
        PanelPostListings.Visible = False
        ' 
        ' ButtonFetchPostListings
        ' 
        ButtonFetchPostListings.FlatStyle = FlatStyle.Popup
        ButtonFetchPostListings.Font = New Font("Segoe UI Variable Display", 9F, FontStyle.Regular, GraphicsUnit.Point)
        ButtonFetchPostListings.ForeColor = Color.Black
        ButtonFetchPostListings.Location = New Point(140, 162)
        ButtonFetchPostListings.Name = "ButtonFetchPostListings"
        ButtonFetchPostListings.Size = New Size(79, 24)
        ButtonFetchPostListings.TabIndex = 31
        ButtonFetchPostListings.Text = "&Fetch"
        ButtonFetchPostListings.UseVisualStyleBackColor = True
        ' 
        ' PanelPostListingsDataHeader
        ' 
        PanelPostListingsDataHeader.BackColor = Color.Transparent
        PanelPostListingsDataHeader.BorderStyle = BorderStyle.FixedSingle
        PanelPostListingsDataHeader.Controls.Add(Label3)
        PanelPostListingsDataHeader.Enabled = False
        PanelPostListingsDataHeader.Location = New Point(3, 0)
        PanelPostListingsDataHeader.Name = "PanelPostListingsDataHeader"
        PanelPostListingsDataHeader.Size = New Size(215, 20)
        PanelPostListingsDataHeader.TabIndex = 30
        ' 
        ' Label3
        ' 
        Label3.AutoSize = True
        Label3.BackColor = Color.Transparent
        Label3.Font = New Font("Segoe UI Variable Display Semib", 9F, FontStyle.Bold, GraphicsUnit.Point)
        Label3.ForeColor = Color.Black
        Label3.Location = New Point(35, 0)
        Label3.Name = "Label3"
        Label3.Size = New Size(147, 16)
        Label3.TabIndex = 29
        Label3.Text = "Fetch posts from a Listing"
        ' 
        ' GroupBoxPostListingsFiltering
        ' 
        GroupBoxPostListingsFiltering.Controls.Add(LabelPostListingsListing)
        GroupBoxPostListingsFiltering.Controls.Add(LabelPostListingsLimit)
        GroupBoxPostListingsFiltering.Controls.Add(NumericUpDownPostListingsLimit)
        GroupBoxPostListingsFiltering.Controls.Add(ComboBoxPostListingsListing)
        GroupBoxPostListingsFiltering.Font = New Font("Segoe UI Variable Display", 8.25F, FontStyle.Underline, GraphicsUnit.Point)
        GroupBoxPostListingsFiltering.Location = New Point(3, 91)
        GroupBoxPostListingsFiltering.Name = "GroupBoxPostListingsFiltering"
        GroupBoxPostListingsFiltering.Size = New Size(215, 69)
        GroupBoxPostListingsFiltering.TabIndex = 27
        GroupBoxPostListingsFiltering.TabStop = False
        GroupBoxPostListingsFiltering.Text = "Set posts sort criterion and output limit"
        ' 
        ' LabelPostListingsListing
        ' 
        LabelPostListingsListing.AutoSize = True
        LabelPostListingsListing.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        LabelPostListingsListing.Location = New Point(4, 22)
        LabelPostListingsListing.Name = "LabelPostListingsListing"
        LabelPostListingsListing.Size = New Size(72, 15)
        LabelPostListingsListing.TabIndex = 18
        LabelPostListingsListing.Text = "Sort posts by:"
        ' 
        ' LabelPostListingsLimit
        ' 
        LabelPostListingsLimit.AutoSize = True
        LabelPostListingsLimit.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        LabelPostListingsLimit.Location = New Point(126, 23)
        LabelPostListingsLimit.Name = "LabelPostListingsLimit"
        LabelPostListingsLimit.Size = New Size(81, 15)
        LabelPostListingsLimit.TabIndex = 19
        LabelPostListingsLimit.Text = "Limit output to:"
        ' 
        ' NumericUpDownPostListingsLimit
        ' 
        NumericUpDownPostListingsLimit.Font = New Font("Segoe UI Variable Display Semib", 8.25F, FontStyle.Bold, GraphicsUnit.Point)
        NumericUpDownPostListingsLimit.Location = New Point(130, 41)
        NumericUpDownPostListingsLimit.Minimum = New Decimal(New Integer() {5, 0, 0, 0})
        NumericUpDownPostListingsLimit.Name = "NumericUpDownPostListingsLimit"
        NumericUpDownPostListingsLimit.ReadOnly = True
        NumericUpDownPostListingsLimit.Size = New Size(79, 22)
        NumericUpDownPostListingsLimit.TabIndex = 17
        NumericUpDownPostListingsLimit.Value = New Decimal(New Integer() {10, 0, 0, 0})
        ' 
        ' GroupBoxPostListings
        ' 
        GroupBoxPostListings.BackColor = Color.Transparent
        GroupBoxPostListings.ContextMenuStrip = ContextMenuStripRightClick
        GroupBoxPostListings.Controls.Add(RadioButtonControversial)
        GroupBoxPostListings.Controls.Add(RadioButtonBest)
        GroupBoxPostListings.Controls.Add(RadioButtonPopular)
        GroupBoxPostListings.Controls.Add(RadioButtonRising)
        GroupBoxPostListings.FlatStyle = FlatStyle.Flat
        GroupBoxPostListings.Font = New Font("Segoe UI Variable Display", 8.25F, FontStyle.Underline, GraphicsUnit.Point)
        GroupBoxPostListings.Location = New Point(3, 23)
        GroupBoxPostListings.Name = "GroupBoxPostListings"
        GroupBoxPostListings.Size = New Size(215, 67)
        GroupBoxPostListings.TabIndex = 26
        GroupBoxPostListings.TabStop = False
        GroupBoxPostListings.Text = "Fetch posts from selected listing"
        ' 
        ' PanelSearchPosts
        ' 
        PanelSearchPosts.Controls.Add(ButtonSearch)
        PanelSearchPosts.Controls.Add(Panel1)
        PanelSearchPosts.Controls.Add(TextBoxQuery)
        PanelSearchPosts.Controls.Add(GroupBoxSearchResultsFiltering)
        PanelSearchPosts.Location = New Point(147, 12)
        PanelSearchPosts.Name = "PanelSearchPosts"
        PanelSearchPosts.Size = New Size(221, 188)
        PanelSearchPosts.TabIndex = 27
        PanelSearchPosts.Visible = False
        ' 
        ' Panel1
        ' 
        Panel1.BackColor = Color.Transparent
        Panel1.BorderStyle = BorderStyle.FixedSingle
        Panel1.Controls.Add(Label4)
        Panel1.Enabled = False
        Panel1.Location = New Point(3, 0)
        Panel1.Name = "Panel1"
        Panel1.Size = New Size(215, 20)
        Panel1.TabIndex = 31
        ' 
        ' Label4
        ' 
        Label4.AutoSize = True
        Label4.BackColor = Color.Transparent
        Label4.Font = New Font("Segoe UI Variable Display Semib", 9F, FontStyle.Bold, GraphicsUnit.Point)
        Label4.ForeColor = Color.Black
        Label4.Location = New Point(64, 0)
        Label4.Name = "Label4"
        Label4.Size = New Size(76, 16)
        Label4.TabIndex = 29
        Label4.Text = "Search posts"
        ' 
        ' NotifyIcon1
        ' 
        NotifyIcon1.BalloonTipIcon = ToolTipIcon.Info
        NotifyIcon1.BalloonTipText = "Knew Karma"
        NotifyIcon1.BalloonTipTitle = "Quick Actions"
        NotifyIcon1.ContextMenuStrip = ContextMenuStripRightClick
        NotifyIcon1.Icon = CType(resources.GetObject("NotifyIcon1.Icon"), Icon)
        NotifyIcon1.Text = "Knew Karma"
        NotifyIcon1.Visible = True
        ' 
        ' PanelPostData
        ' 
        PanelPostData.BackColor = Color.Transparent
        PanelPostData.Controls.Add(TextBoxPostSubreddit)
        PanelPostData.Controls.Add(ButtonFetchPostData)
        PanelPostData.Controls.Add(PanelPostDataHeader)
        PanelPostData.Controls.Add(TextBoxPostID)
        PanelPostData.Controls.Add(GroupBoxPostDataFiltering)
        PanelPostData.Controls.Add(GroupBoxPostData)
        PanelPostData.Enabled = False
        PanelPostData.ForeColor = Color.Black
        PanelPostData.Location = New Point(147, 12)
        PanelPostData.Name = "PanelPostData"
        PanelPostData.Size = New Size(221, 188)
        PanelPostData.TabIndex = 28
        PanelPostData.Visible = False
        ' 
        ' TextBoxPostSubreddit
        ' 
        TextBoxPostSubreddit.Font = New Font("Segoe UI Variable Display Semib", 9F, FontStyle.Bold, GraphicsUnit.Point)
        TextBoxPostSubreddit.Location = New Point(69, 162)
        TextBoxPostSubreddit.Name = "TextBoxPostSubreddit"
        TextBoxPostSubreddit.PlaceholderText = "Subreddit"
        TextBoxPostSubreddit.Size = New Size(65, 23)
        TextBoxPostSubreddit.TabIndex = 31
        ' 
        ' ButtonFetchPostData
        ' 
        ButtonFetchPostData.FlatStyle = FlatStyle.Popup
        ButtonFetchPostData.Font = New Font("Segoe UI Variable Display", 9F, FontStyle.Regular, GraphicsUnit.Point)
        ButtonFetchPostData.ForeColor = Color.Black
        ButtonFetchPostData.Location = New Point(140, 162)
        ButtonFetchPostData.Name = "ButtonFetchPostData"
        ButtonFetchPostData.Size = New Size(79, 24)
        ButtonFetchPostData.TabIndex = 6
        ButtonFetchPostData.Text = "&Fetch"
        ButtonFetchPostData.UseVisualStyleBackColor = True
        ' 
        ' PanelPostDataHeader
        ' 
        PanelPostDataHeader.BackColor = Color.Transparent
        PanelPostDataHeader.BorderStyle = BorderStyle.FixedSingle
        PanelPostDataHeader.Controls.Add(Label6)
        PanelPostDataHeader.Enabled = False
        PanelPostDataHeader.Location = New Point(3, 0)
        PanelPostDataHeader.Name = "PanelPostDataHeader"
        PanelPostDataHeader.Size = New Size(215, 20)
        PanelPostDataHeader.TabIndex = 30
        ' 
        ' Label6
        ' 
        Label6.AutoSize = True
        Label6.BackColor = Color.Transparent
        Label6.Font = New Font("Segoe UI Variable Display Semib", 9F, FontStyle.Bold, GraphicsUnit.Point)
        Label6.ForeColor = Color.Black
        Label6.Location = New Point(48, 0)
        Label6.Name = "Label6"
        Label6.Size = New Size(108, 16)
        Label6.TabIndex = 29
        Label6.Text = "Fetch a Post's data"
        ' 
        ' TextBoxPostID
        ' 
        TextBoxPostID.Font = New Font("Segoe UI Variable Display Semib", 9F, FontStyle.Bold, GraphicsUnit.Point)
        TextBoxPostID.Location = New Point(3, 162)
        TextBoxPostID.Name = "TextBoxPostID"
        TextBoxPostID.PlaceholderText = "Post ID"
        TextBoxPostID.Size = New Size(62, 23)
        TextBoxPostID.TabIndex = 5
        ' 
        ' GroupBoxPostDataFiltering
        ' 
        GroupBoxPostDataFiltering.Controls.Add(Label7)
        GroupBoxPostDataFiltering.Controls.Add(Label8)
        GroupBoxPostDataFiltering.Controls.Add(NumericUpDownPostDataLimit)
        GroupBoxPostDataFiltering.Controls.Add(ComboBoxPostDataListing)
        GroupBoxPostDataFiltering.Font = New Font("Segoe UI Variable Display", 8.25F, FontStyle.Underline, GraphicsUnit.Point)
        GroupBoxPostDataFiltering.ForeColor = Color.Black
        GroupBoxPostDataFiltering.Location = New Point(3, 81)
        GroupBoxPostDataFiltering.Name = "GroupBoxPostDataFiltering"
        GroupBoxPostDataFiltering.Size = New Size(215, 70)
        GroupBoxPostDataFiltering.TabIndex = 11
        GroupBoxPostDataFiltering.TabStop = False
        GroupBoxPostDataFiltering.Text = "Set data sort criterion and output limit"
        ' 
        ' Label7
        ' 
        Label7.AutoSize = True
        Label7.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        Label7.Location = New Point(126, 23)
        Label7.Name = "Label7"
        Label7.Size = New Size(81, 15)
        Label7.TabIndex = 19
        Label7.Text = "Limit output to:"
        ' 
        ' Label8
        ' 
        Label8.AutoSize = True
        Label8.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        Label8.Location = New Point(4, 22)
        Label8.Name = "Label8"
        Label8.Size = New Size(68, 15)
        Label8.TabIndex = 18
        Label8.Text = "Sort data by:"
        ' 
        ' NumericUpDownPostDataLimit
        ' 
        NumericUpDownPostDataLimit.Enabled = False
        NumericUpDownPostDataLimit.Font = New Font("Segoe UI Variable Display Semib", 8.25F, FontStyle.Bold, GraphicsUnit.Point)
        NumericUpDownPostDataLimit.Location = New Point(130, 41)
        NumericUpDownPostDataLimit.Minimum = New Decimal(New Integer() {5, 0, 0, 0})
        NumericUpDownPostDataLimit.Name = "NumericUpDownPostDataLimit"
        NumericUpDownPostDataLimit.ReadOnly = True
        NumericUpDownPostDataLimit.Size = New Size(79, 22)
        NumericUpDownPostDataLimit.TabIndex = 17
        NumericUpDownPostDataLimit.Value = New Decimal(New Integer() {10, 0, 0, 0})
        ' 
        ' ComboBoxPostDataListing
        ' 
        ComboBoxPostDataListing.AutoCompleteCustomSource.AddRange(New String() {"Controversial", "Hot", "Best", "New", "Rising"})
        ComboBoxPostDataListing.AutoCompleteSource = AutoCompleteSource.CustomSource
        ComboBoxPostDataListing.BackColor = SystemColors.Window
        ComboBoxPostDataListing.DropDownStyle = ComboBoxStyle.DropDownList
        ComboBoxPostDataListing.Enabled = False
        ComboBoxPostDataListing.FlatStyle = FlatStyle.Popup
        ComboBoxPostDataListing.Font = New Font("Segoe UI Variable Display Semib", 8.25F, FontStyle.Bold, GraphicsUnit.Point)
        ComboBoxPostDataListing.ForeColor = SystemColors.WindowText
        ComboBoxPostDataListing.FormattingEnabled = True
        ComboBoxPostDataListing.Items.AddRange(New Object() {"all", "best", "controversial", "hot", "new", "rising", "top"})
        ComboBoxPostDataListing.Location = New Point(6, 40)
        ComboBoxPostDataListing.Name = "ComboBoxPostDataListing"
        ComboBoxPostDataListing.Size = New Size(116, 23)
        ComboBoxPostDataListing.Sorted = True
        ComboBoxPostDataListing.TabIndex = 11
        ' 
        ' GroupBoxPostData
        ' 
        GroupBoxPostData.BackColor = Color.Transparent
        GroupBoxPostData.ContextMenuStrip = ContextMenuStripRightClick
        GroupBoxPostData.Controls.Add(RadioButtonPostProfile)
        GroupBoxPostData.Controls.Add(RadioButtonPostComments)
        GroupBoxPostData.FlatStyle = FlatStyle.Flat
        GroupBoxPostData.Font = New Font("Segoe UI Variable Display", 8.25F, FontStyle.Underline, GraphicsUnit.Point)
        GroupBoxPostData.ForeColor = Color.Black
        GroupBoxPostData.Location = New Point(3, 26)
        GroupBoxPostData.Name = "GroupBoxPostData"
        GroupBoxPostData.Size = New Size(215, 49)
        GroupBoxPostData.TabIndex = 9
        GroupBoxPostData.TabStop = False
        GroupBoxPostData.Text = "Select subreddit data to fetch"
        ' 
        ' RadioButtonPostProfile
        ' 
        RadioButtonPostProfile.AutoSize = True
        RadioButtonPostProfile.Checked = True
        RadioButtonPostProfile.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        RadioButtonPostProfile.Location = New Point(6, 23)
        RadioButtonPostProfile.Name = "RadioButtonPostProfile"
        RadioButtonPostProfile.Size = New Size(56, 19)
        RadioButtonPostProfile.TabIndex = 5
        RadioButtonPostProfile.TabStop = True
        RadioButtonPostProfile.Text = "Profile"
        RadioButtonPostProfile.UseVisualStyleBackColor = True
        ' 
        ' RadioButtonPostComments
        ' 
        RadioButtonPostComments.AutoSize = True
        RadioButtonPostComments.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        RadioButtonPostComments.Location = New Point(71, 23)
        RadioButtonPostComments.Name = "RadioButtonPostComments"
        RadioButtonPostComments.Size = New Size(77, 19)
        RadioButtonPostComments.TabIndex = 6
        RadioButtonPostComments.Text = "Comments"
        RadioButtonPostComments.UseVisualStyleBackColor = True
        ' 
        ' Main
        ' 
        AccessibleRole = AccessibleRole.Window
        AutoScaleDimensions = New SizeF(7F, 16F)
        AutoScaleMode = AutoScaleMode.Font
        BackColor = Color.White
        ClientSize = New Size(377, 211)
        ContextMenuStrip = ContextMenuStripRightClick
        Controls.Add(PanelPostData)
        Controls.Add(PanelSubredditData)
        Controls.Add(PanelSearchPosts)
        Controls.Add(PanelPostListings)
        Controls.Add(PanelFrontPageData)
        Controls.Add(PanelUserData)
        Controls.Add(TreeView1)
        Font = New Font("Segoe UI Variable Display", 9F, FontStyle.Regular, GraphicsUnit.Point)
        ForeColor = Color.Black
        FormBorderStyle = FormBorderStyle.FixedDialog
        HelpButton = True
        Icon = CType(resources.GetObject("$this.Icon"), Icon)
        MaximizeBox = False
        MinimizeBox = False
        Name = "Main"
        StartPosition = FormStartPosition.CenterScreen
        ContextMenuStripRightClick.ResumeLayout(False)
        GroupBoxSearchResultsFiltering.ResumeLayout(False)
        GroupBoxSearchResultsFiltering.PerformLayout()
        CType(NumericUpDownSearchResultLimit, ComponentModel.ISupportInitialize).EndInit()
        GroupBoxFrontPageDataFiltering.ResumeLayout(False)
        GroupBoxFrontPageDataFiltering.PerformLayout()
        CType(NumericUpDownFrontPageDataLimit, ComponentModel.ISupportInitialize).EndInit()
        GroupBoxSubredditDataFiltering.ResumeLayout(False)
        GroupBoxSubredditDataFiltering.PerformLayout()
        CType(NumericUpDownSubredditDataLimit, ComponentModel.ISupportInitialize).EndInit()
        GroupBoxSubredditData.ResumeLayout(False)
        GroupBoxSubredditData.PerformLayout()
        GroupBoxUserDataFiltering.ResumeLayout(False)
        GroupBoxUserDataFiltering.PerformLayout()
        CType(NumericUpDownUserDataLimit, ComponentModel.ISupportInitialize).EndInit()
        GroupBoxUserData.ResumeLayout(False)
        GroupBoxUserData.PerformLayout()
        PanelUserData.ResumeLayout(False)
        PanelUserData.PerformLayout()
        PanelUserDataHeader.ResumeLayout(False)
        PanelUserDataHeader.PerformLayout()
        PanelSubredditData.ResumeLayout(False)
        PanelSubredditData.PerformLayout()
        PanelSubredditDataHeader.ResumeLayout(False)
        PanelSubredditDataHeader.PerformLayout()
        PanelFrontPageData.ResumeLayout(False)
        PanelFrontPageHeader.ResumeLayout(False)
        PanelFrontPageHeader.PerformLayout()
        PanelPostListings.ResumeLayout(False)
        PanelPostListingsDataHeader.ResumeLayout(False)
        PanelPostListingsDataHeader.PerformLayout()
        GroupBoxPostListingsFiltering.ResumeLayout(False)
        GroupBoxPostListingsFiltering.PerformLayout()
        CType(NumericUpDownPostListingsLimit, ComponentModel.ISupportInitialize).EndInit()
        GroupBoxPostListings.ResumeLayout(False)
        GroupBoxPostListings.PerformLayout()
        PanelSearchPosts.ResumeLayout(False)
        PanelSearchPosts.PerformLayout()
        Panel1.ResumeLayout(False)
        Panel1.PerformLayout()
        PanelPostData.ResumeLayout(False)
        PanelPostData.PerformLayout()
        PanelPostDataHeader.ResumeLayout(False)
        PanelPostDataHeader.PerformLayout()
        GroupBoxPostDataFiltering.ResumeLayout(False)
        GroupBoxPostDataFiltering.PerformLayout()
        CType(NumericUpDownPostDataLimit, ComponentModel.ISupportInitialize).EndInit()
        GroupBoxPostData.ResumeLayout(False)
        GroupBoxPostData.PerformLayout()
        ResumeLayout(False)
    End Sub

    Friend WithEvents TextBoxQuery As TextBox
    Friend WithEvents ButtonSearch As Button
    Friend WithEvents ContextMenuStripRightClick As ContextMenuStrip
    Friend WithEvents SaveDataToolStripMenuItem As ToolStripMenuItem
    Friend WithEvents ToJSONToolStripMenuItem As ToolStripMenuItem
    Friend WithEvents ToCSVToolStripMenuItem As ToolStripMenuItem
    Friend WithEvents AboutToolStripMenuItem As ToolStripMenuItem
    Friend WithEvents ExitToolStripMenuItem As ToolStripMenuItem
    Friend WithEvents SettingsToolStripMenuItem As ToolStripMenuItem
    Friend WithEvents DarkModeToolStripMenuItem As ToolStripMenuItem
    Friend WithEvents SaveFoundPostsToolStripMenuItem As ToolStripMenuItem
    Friend WithEvents TextBoxUsername As TextBox
    Friend WithEvents ButtonFetchUserData As Button
    Friend WithEvents TextBoxSubreddit As TextBox
    Friend WithEvents ButtonFetchSubredditData As Button
    Friend WithEvents RadioButtonUserPosts As RadioButton
    Friend WithEvents RadioButtonUserProfile As RadioButton
    Friend WithEvents RadioButtonUserComments As RadioButton
    Friend WithEvents GroupBoxUserData As GroupBox
    Friend WithEvents GroupBoxSubredditData As GroupBox
    Friend WithEvents RadioButtonSubredditProfile As RadioButton
    Friend WithEvents RadioButtonSubredditPosts As RadioButton
    Friend WithEvents GroupBoxUserDataFiltering As GroupBox
    Friend WithEvents ComboBoxUserPostsListing As ComboBox
    Friend WithEvents NumericUpDownUserDataLimit As NumericUpDown
    Friend WithEvents LabelUserDataLimit As Label
    Friend WithEvents LabelUserPostsListing As Label
    Friend WithEvents GroupBoxSearchResultsFiltering As GroupBox
    Friend WithEvents LabelSearchResultsLimit As Label
    Friend WithEvents LabelSearchResultsListing As Label
    Friend WithEvents NumericUpDownSearchResultLimit As NumericUpDown
    Friend WithEvents ComboBoxSearchResultListing As ComboBox
    Friend WithEvents GroupBoxSubredditDataFiltering As GroupBox
    Friend WithEvents LabelSubredditDataLimit As Label
    Friend WithEvents LabelSubredditPostsListing As Label
    Friend WithEvents NumericUpDownSubredditDataLimit As NumericUpDown
    Friend WithEvents ComboBoxSubredditPostsListing As ComboBox
    Friend WithEvents NumericUpDown2 As NumericUpDown
    Friend WithEvents ButtonFetchFrontPageData As Button
    Friend WithEvents PictureBox1 As PictureBox
    Friend WithEvents GroupBoxFrontPageDataFiltering As GroupBox
    Friend WithEvents LabelFrontPageDataLimit As Label
    Friend WithEvents LabelFrontPageDataListing As Label
    Friend WithEvents NumericUpDownFrontPageDataLimit As NumericUpDown
    Friend WithEvents ComboBoxFrontPageDataListing As ComboBox
    Friend WithEvents TreeView1 As TreeView
    Friend WithEvents PanelUserData As Panel
    Friend WithEvents PanelSubredditData As Panel
    Friend WithEvents PanelFrontPageData As Panel
    Friend WithEvents PanelPostListings As Panel
    Friend WithEvents GroupBoxPostListings As GroupBox
    Friend WithEvents RadioButtonBest As RadioButton
    Friend WithEvents RadioButtonPopular As RadioButton
    Friend WithEvents RadioButtonRising As RadioButton
    Friend WithEvents LabelPostListingsLimit As Label
    Friend WithEvents RadioButtonControversial As RadioButton
    Friend WithEvents GroupBoxPostListingsFiltering As GroupBox
    Friend WithEvents LabelPostListingsListing As Label
    Friend WithEvents NumericUpDownPostListingsLimit As NumericUpDown
    Friend WithEvents ComboBoxPostListingsListing As ComboBox
    Friend WithEvents PanelSearchPosts As Panel
    Friend WithEvents GroupBoxUser As GroupBox
    Friend WithEvents DarkModeEnableToolStripMenuItem As ToolStripMenuItem
    Friend WithEvents DarkModeDisableToolStripMenuItem As ToolStripMenuItem
    Friend WithEvents PanelUserDataHeader As Panel
    Friend WithEvents Label1 As Label
    Friend WithEvents PanelSubredditDataHeader As Panel
    Friend WithEvents Label2 As Label
    Friend WithEvents PanelPostListingsDataHeader As Panel
    Friend WithEvents Label3 As Label
    Friend WithEvents Panel1 As Panel
    Friend WithEvents Label4 As Label
    Friend WithEvents PanelFrontPageHeader As Panel
    Friend WithEvents Label5 As Label
    Friend WithEvents NotifyIcon1 As NotifyIcon
    Friend WithEvents ButtonFetchPostListings As Button
    Friend WithEvents PanelPostData As Panel
    Friend WithEvents ButtonFetchPostData As Button
    Friend WithEvents PanelPostDataHeader As Panel
    Friend WithEvents Label6 As Label
    Friend WithEvents TextBoxPostID As TextBox
    Friend WithEvents GroupBoxPostDataFiltering As GroupBox
    Friend WithEvents Label7 As Label
    Friend WithEvents Label8 As Label
    Friend WithEvents NumericUpDownPostDataLimit As NumericUpDown
    Friend WithEvents ComboBoxPostDataListing As ComboBox
    Friend WithEvents GroupBoxPostData As GroupBox
    Friend WithEvents RadioButtonPostProfile As RadioButton
    Friend WithEvents RadioButtonPostComments As RadioButton
    Friend WithEvents TextBoxPostSubreddit As TextBox
End Class
