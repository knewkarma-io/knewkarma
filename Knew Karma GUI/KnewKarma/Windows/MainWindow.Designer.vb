<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()>
Partial Class MainWindow
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
        Dim resources As System.ComponentModel.ComponentResourceManager = New System.ComponentModel.ComponentResourceManager(GetType(MainWindow))
        Dim TreeNode1 As TreeNode = New TreeNode("User")
        Dim TreeNode2 As TreeNode = New TreeNode("Community")
        Dim TreeNode3 As TreeNode = New TreeNode("Search")
        Dim TreeNode4 As TreeNode = New TreeNode("Listings")
        Dim TreeNode5 As TreeNode = New TreeNode("Front-Page/New")
        Dim TreeNode6 As TreeNode = New TreeNode("Posts", New TreeNode() {TreeNode4, TreeNode5})
        Dim TreeNode7 As TreeNode = New TreeNode("Username", New TreeNode() {TreeNode1, TreeNode2, TreeNode3, TreeNode6})
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
        TextBoxCommunity = New TextBox()
        RadioButtonUserComments = New RadioButton()
        RadioButtonUserPosts = New RadioButton()
        RadioButtonUserProfile = New RadioButton()
        RadioButtonCommunityProfile = New RadioButton()
        RadioButtonCommunityPosts = New RadioButton()
        ComboBoxUserDataListing = New ComboBox()
        ComboBoxSearchResultListing = New ComboBox()
        ComboBoxCommunityPostsListing = New ComboBox()
        ComboBoxFrontPageAndNewPostsListing = New ComboBox()
        RadioButtonBest = New RadioButton()
        RadioButtonPopular = New RadioButton()
        RadioButtonRising = New RadioButton()
        RadioButtonControversial = New RadioButton()
        ComboBoxPostListingsListing = New ComboBox()
        GroupBoxSearchResultsFiltering = New GroupBox()
        LabelSearchResultsLimit = New Label()
        LabelSearchResultsListing = New Label()
        NumericUpDownSearchResultLimit = New NumericUpDown()
        GroupBoxFrontPageAndNewPostsFiltering = New GroupBox()
        LabelFrontPageDataLimit = New Label()
        LabelFrontPageDataListing = New Label()
        NumericUpDownFrontPageAndNewPostsLimit = New NumericUpDown()
        ButtonGetFrontPageAndNewPosts = New Button()
        GroupBoxCommunityDataFiltering = New GroupBox()
        LabelCommunityPostsLimit = New Label()
        LabelCommunityPostsListing = New Label()
        NumericUpDownCommunityPostsLimit = New NumericUpDown()
        ButtonGetCommunityData = New Button()
        GroupBoxCommunityData = New GroupBox()
        GroupBoxUserDataFiltering = New GroupBox()
        LabelUserDataLimit = New Label()
        LabelUserPostsListing = New Label()
        NumericUpDownUserDataLimit = New NumericUpDown()
        ButtonGetUserData = New Button()
        GroupBoxUserData = New GroupBox()
        TreeView1 = New TreeView()
        PanelUserData = New Panel()
        PanelUserDataHeader = New Panel()
        Label1 = New Label()
        PanelCommunityData = New Panel()
        PanelCommunityDataHeader = New Panel()
        Label2 = New Label()
        PanelFrontPageAndNew = New Panel()
        GroupBoxFrontPageAndNewPosts = New GroupBox()
        RadioButtonNewPosts = New RadioButton()
        RadioButtonFrontPagePosts = New RadioButton()
        PanelFrontPageAndNewHeader = New Panel()
        Label5 = New Label()
        PanelPostListings = New Panel()
        ButtonGetListingPosts = New Button()
        PanelPostListingsDataHeader = New Panel()
        Label3 = New Label()
        GroupBoxPostListingsFiltering = New GroupBox()
        LabelPostListingsListing = New Label()
        LabelPostListingsLimit = New Label()
        NumericUpDownPostListingsLimit = New NumericUpDown()
        GroupBoxPostListings = New GroupBox()
        PanelSearch = New Panel()
        GroupBoxSearchData = New GroupBox()
        RadioButtonSearchCommunities = New RadioButton()
        RadioButtonSearchUsers = New RadioButton()
        RadioButtonSearchPosts = New RadioButton()
        Panel1 = New Panel()
        Label4 = New Label()
        NotifyIcon1 = New NotifyIcon(components)
        PanelHome = New Panel()
        LabelProgramLastName = New Label()
        LabelProgramFirstName = New Label()
        Panel3 = New Panel()
        Label6 = New Label()
        ContextMenuStripRightClick.SuspendLayout()
        GroupBoxSearchResultsFiltering.SuspendLayout()
        CType(NumericUpDownSearchResultLimit, ComponentModel.ISupportInitialize).BeginInit()
        GroupBoxFrontPageAndNewPostsFiltering.SuspendLayout()
        CType(NumericUpDownFrontPageAndNewPostsLimit, ComponentModel.ISupportInitialize).BeginInit()
        GroupBoxCommunityDataFiltering.SuspendLayout()
        CType(NumericUpDownCommunityPostsLimit, ComponentModel.ISupportInitialize).BeginInit()
        GroupBoxCommunityData.SuspendLayout()
        GroupBoxUserDataFiltering.SuspendLayout()
        CType(NumericUpDownUserDataLimit, ComponentModel.ISupportInitialize).BeginInit()
        GroupBoxUserData.SuspendLayout()
        PanelUserData.SuspendLayout()
        PanelUserDataHeader.SuspendLayout()
        PanelCommunityData.SuspendLayout()
        PanelCommunityDataHeader.SuspendLayout()
        PanelFrontPageAndNew.SuspendLayout()
        GroupBoxFrontPageAndNewPosts.SuspendLayout()
        PanelFrontPageAndNewHeader.SuspendLayout()
        PanelPostListings.SuspendLayout()
        PanelPostListingsDataHeader.SuspendLayout()
        GroupBoxPostListingsFiltering.SuspendLayout()
        CType(NumericUpDownPostListingsLimit, ComponentModel.ISupportInitialize).BeginInit()
        GroupBoxPostListings.SuspendLayout()
        PanelSearch.SuspendLayout()
        GroupBoxSearchData.SuspendLayout()
        Panel1.SuspendLayout()
        PanelHome.SuspendLayout()
        Panel3.SuspendLayout()
        SuspendLayout()
        ' 
        ' TextBoxQuery
        ' 
        TextBoxQuery.BackColor = SystemColors.Window
        TextBoxQuery.Font = New Font("Segoe UI Variable Display Semib", 9.0F, FontStyle.Bold, GraphicsUnit.Point)
        TextBoxQuery.ForeColor = SystemColors.WindowText
        TextBoxQuery.Location = New Point(3, 163)
        TextBoxQuery.Name = "TextBoxQuery"
        TextBoxQuery.PlaceholderText = "Search query (e.g., osint)"
        TextBoxQuery.Size = New Size(148, 23)
        TextBoxQuery.TabIndex = 0
        ' 
        ' ButtonSearch
        ' 
        ButtonSearch.FlatStyle = FlatStyle.Popup
        ButtonSearch.Font = New Font("Segoe UI Variable Display", 9.0F, FontStyle.Regular, GraphicsUnit.Point)
        ButtonSearch.ForeColor = Color.Black
        ButtonSearch.Location = New Point(157, 163)
        ButtonSearch.Name = "ButtonSearch"
        ButtonSearch.Size = New Size(62, 24)
        ButtonSearch.TabIndex = 6
        ButtonSearch.Text = "&Search"
        ButtonSearch.UseVisualStyleBackColor = True
        ' 
        ' ContextMenuStripRightClick
        ' 
        ContextMenuStripRightClick.Font = New Font("Segoe UI Variable Text", 9.0F, FontStyle.Regular, GraphicsUnit.Point)
        ContextMenuStripRightClick.Items.AddRange(New ToolStripItem() {AboutToolStripMenuItem, SettingsToolStripMenuItem, ExitToolStripMenuItem})
        ContextMenuStripRightClick.LayoutStyle = ToolStripLayoutStyle.Table
        ContextMenuStripRightClick.Name = "ContextMenuStrip1"
        ContextMenuStripRightClick.Size = New Size(118, 70)
        ContextMenuStripRightClick.Text = "Menu"
        ' 
        ' AboutToolStripMenuItem
        ' 
        AboutToolStripMenuItem.AutoToolTip = True
        AboutToolStripMenuItem.Font = New Font("Segoe UI Variable Display", 9.0F, FontStyle.Regular, GraphicsUnit.Point)
        AboutToolStripMenuItem.Image = CType(resources.GetObject("AboutToolStripMenuItem.Image"), Image)
        AboutToolStripMenuItem.Name = "AboutToolStripMenuItem"
        AboutToolStripMenuItem.Size = New Size(117, 22)
        AboutToolStripMenuItem.Text = "About"
        ' 
        ' SettingsToolStripMenuItem
        ' 
        SettingsToolStripMenuItem.AutoToolTip = True
        SettingsToolStripMenuItem.DropDownItems.AddRange(New ToolStripItem() {DarkModeToolStripMenuItem, SaveDataToolStripMenuItem})
        SettingsToolStripMenuItem.Font = New Font("Segoe UI Variable Display", 9.0F, FontStyle.Regular, GraphicsUnit.Point)
        SettingsToolStripMenuItem.Image = CType(resources.GetObject("SettingsToolStripMenuItem.Image"), Image)
        SettingsToolStripMenuItem.Name = "SettingsToolStripMenuItem"
        SettingsToolStripMenuItem.Size = New Size(117, 22)
        SettingsToolStripMenuItem.Text = "Settings"
        ' 
        ' DarkModeToolStripMenuItem
        ' 
        DarkModeToolStripMenuItem.AutoToolTip = True
        DarkModeToolStripMenuItem.DropDownItems.AddRange(New ToolStripItem() {DarkModeEnableToolStripMenuItem, DarkModeDisableToolStripMenuItem})
        DarkModeToolStripMenuItem.Font = New Font("Segoe UI Variable Display", 9.0F, FontStyle.Regular, GraphicsUnit.Point)
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
        ExitToolStripMenuItem.Font = New Font("Segoe UI Variable Display Semib", 9.0F, FontStyle.Bold, GraphicsUnit.Point)
        ExitToolStripMenuItem.Image = CType(resources.GetObject("ExitToolStripMenuItem.Image"), Image)
        ExitToolStripMenuItem.Name = "ExitToolStripMenuItem"
        ExitToolStripMenuItem.Size = New Size(117, 22)
        ExitToolStripMenuItem.Text = "&Exit"
        ' 
        ' TextBoxUsername
        ' 
        TextBoxUsername.BackColor = SystemColors.Window
        TextBoxUsername.Font = New Font("Segoe UI Variable Display Semib", 9.0F, FontStyle.Bold, GraphicsUnit.Point)
        TextBoxUsername.ForeColor = SystemColors.WindowText
        TextBoxUsername.Location = New Point(3, 163)
        TextBoxUsername.Name = "TextBoxUsername"
        TextBoxUsername.PlaceholderText = "Username (e.g., JohnDoe)"
        TextBoxUsername.Size = New Size(148, 23)
        TextBoxUsername.TabIndex = 1
        ' 
        ' TextBoxCommunity
        ' 
        TextBoxCommunity.Font = New Font("Segoe UI Variable Display Semib", 9.0F, FontStyle.Bold, GraphicsUnit.Point)
        TextBoxCommunity.Location = New Point(3, 163)
        TextBoxCommunity.Name = "TextBoxCommunity"
        TextBoxCommunity.PlaceholderText = "Community (e.g., Ask)"
        TextBoxCommunity.Size = New Size(148, 23)
        TextBoxCommunity.TabIndex = 5
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
        ' RadioButtonCommunityProfile
        ' 
        RadioButtonCommunityProfile.AutoSize = True
        RadioButtonCommunityProfile.Checked = True
        RadioButtonCommunityProfile.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        RadioButtonCommunityProfile.Location = New Point(6, 23)
        RadioButtonCommunityProfile.Name = "RadioButtonCommunityProfile"
        RadioButtonCommunityProfile.Size = New Size(56, 19)
        RadioButtonCommunityProfile.TabIndex = 5
        RadioButtonCommunityProfile.TabStop = True
        RadioButtonCommunityProfile.Text = "Profile"
        RadioButtonCommunityProfile.UseVisualStyleBackColor = True
        ' 
        ' RadioButtonCommunityPosts
        ' 
        RadioButtonCommunityPosts.AutoSize = True
        RadioButtonCommunityPosts.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        RadioButtonCommunityPosts.Location = New Point(71, 23)
        RadioButtonCommunityPosts.Name = "RadioButtonCommunityPosts"
        RadioButtonCommunityPosts.Size = New Size(51, 19)
        RadioButtonCommunityPosts.TabIndex = 6
        RadioButtonCommunityPosts.Text = "Posts"
        RadioButtonCommunityPosts.UseVisualStyleBackColor = True
        ' 
        ' ComboBoxUserDataListing
        ' 
        ComboBoxUserDataListing.AutoCompleteCustomSource.AddRange(New String() {"Controversial", "Hot", "Best", "New", "Rising"})
        ComboBoxUserDataListing.AutoCompleteSource = AutoCompleteSource.CustomSource
        ComboBoxUserDataListing.BackColor = SystemColors.Window
        ComboBoxUserDataListing.DropDownStyle = ComboBoxStyle.DropDownList
        ComboBoxUserDataListing.Enabled = False
        ComboBoxUserDataListing.FlatStyle = FlatStyle.Popup
        ComboBoxUserDataListing.Font = New Font("Segoe UI Variable Display Semib", 8.25F, FontStyle.Bold, GraphicsUnit.Point)
        ComboBoxUserDataListing.ForeColor = SystemColors.WindowText
        ComboBoxUserDataListing.FormattingEnabled = True
        ComboBoxUserDataListing.Items.AddRange(New Object() {"all", "best", "controversial", "hot", "new", "rising", "top"})
        ComboBoxUserDataListing.Location = New Point(6, 40)
        ComboBoxUserDataListing.Name = "ComboBoxUserDataListing"
        ComboBoxUserDataListing.Size = New Size(116, 23)
        ComboBoxUserDataListing.Sorted = True
        ComboBoxUserDataListing.TabIndex = 11
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
        ' ComboBoxCommunityPostsListing
        ' 
        ComboBoxCommunityPostsListing.AutoCompleteCustomSource.AddRange(New String() {"Controversial", "Hot", "Best", "New", "Rising"})
        ComboBoxCommunityPostsListing.AutoCompleteSource = AutoCompleteSource.CustomSource
        ComboBoxCommunityPostsListing.BackColor = SystemColors.Window
        ComboBoxCommunityPostsListing.DropDownStyle = ComboBoxStyle.DropDownList
        ComboBoxCommunityPostsListing.Enabled = False
        ComboBoxCommunityPostsListing.FlatStyle = FlatStyle.Popup
        ComboBoxCommunityPostsListing.Font = New Font("Segoe UI Variable Display Semib", 8.25F, FontStyle.Bold, GraphicsUnit.Point)
        ComboBoxCommunityPostsListing.ForeColor = SystemColors.WindowText
        ComboBoxCommunityPostsListing.FormattingEnabled = True
        ComboBoxCommunityPostsListing.Items.AddRange(New Object() {"all", "best", "controversial", "hot", "new", "rising", "top"})
        ComboBoxCommunityPostsListing.Location = New Point(6, 40)
        ComboBoxCommunityPostsListing.Name = "ComboBoxCommunityPostsListing"
        ComboBoxCommunityPostsListing.Size = New Size(116, 23)
        ComboBoxCommunityPostsListing.Sorted = True
        ComboBoxCommunityPostsListing.TabIndex = 11
        ' 
        ' ComboBoxFrontPageAndNewPostsListing
        ' 
        ComboBoxFrontPageAndNewPostsListing.AutoCompleteCustomSource.AddRange(New String() {"Controversial", "Hot", "Best", "New", "Rising"})
        ComboBoxFrontPageAndNewPostsListing.AutoCompleteSource = AutoCompleteSource.CustomSource
        ComboBoxFrontPageAndNewPostsListing.BackColor = SystemColors.Window
        ComboBoxFrontPageAndNewPostsListing.DropDownStyle = ComboBoxStyle.DropDownList
        ComboBoxFrontPageAndNewPostsListing.FlatStyle = FlatStyle.Popup
        ComboBoxFrontPageAndNewPostsListing.Font = New Font("Segoe UI Variable Display Semib", 8.25F, FontStyle.Bold, GraphicsUnit.Point)
        ComboBoxFrontPageAndNewPostsListing.ForeColor = SystemColors.WindowText
        ComboBoxFrontPageAndNewPostsListing.FormattingEnabled = True
        ComboBoxFrontPageAndNewPostsListing.Items.AddRange(New Object() {"all", "best", "controversial", "hot", "new", "rising", "top"})
        ComboBoxFrontPageAndNewPostsListing.Location = New Point(6, 40)
        ComboBoxFrontPageAndNewPostsListing.Name = "ComboBoxFrontPageAndNewPostsListing"
        ComboBoxFrontPageAndNewPostsListing.Size = New Size(116, 23)
        ComboBoxFrontPageAndNewPostsListing.Sorted = True
        ComboBoxFrontPageAndNewPostsListing.TabIndex = 11
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
        GroupBoxSearchResultsFiltering.Location = New Point(3, 81)
        GroupBoxSearchResultsFiltering.Name = "GroupBoxSearchResultsFiltering"
        GroupBoxSearchResultsFiltering.Size = New Size(215, 70)
        GroupBoxSearchResultsFiltering.TabIndex = 11
        GroupBoxSearchResultsFiltering.TabStop = False
        GroupBoxSearchResultsFiltering.Text = "Set results sort criterion and limit"
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
        NumericUpDownSearchResultLimit.Maximum = New Decimal(New Integer() {10000, 0, 0, 0})
        NumericUpDownSearchResultLimit.Minimum = New Decimal(New Integer() {1, 0, 0, 0})
        NumericUpDownSearchResultLimit.Name = "NumericUpDownSearchResultLimit"
        NumericUpDownSearchResultLimit.ReadOnly = True
        NumericUpDownSearchResultLimit.Size = New Size(79, 22)
        NumericUpDownSearchResultLimit.TabIndex = 17
        NumericUpDownSearchResultLimit.Value = New Decimal(New Integer() {100, 0, 0, 0})
        ' 
        ' GroupBoxFrontPageAndNewPostsFiltering
        ' 
        GroupBoxFrontPageAndNewPostsFiltering.Controls.Add(LabelFrontPageDataLimit)
        GroupBoxFrontPageAndNewPostsFiltering.Controls.Add(LabelFrontPageDataListing)
        GroupBoxFrontPageAndNewPostsFiltering.Controls.Add(NumericUpDownFrontPageAndNewPostsLimit)
        GroupBoxFrontPageAndNewPostsFiltering.Controls.Add(ComboBoxFrontPageAndNewPostsListing)
        GroupBoxFrontPageAndNewPostsFiltering.Font = New Font("Segoe UI Variable Display", 8.25F, FontStyle.Underline, GraphicsUnit.Point)
        GroupBoxFrontPageAndNewPostsFiltering.Location = New Point(3, 81)
        GroupBoxFrontPageAndNewPostsFiltering.Name = "GroupBoxFrontPageAndNewPostsFiltering"
        GroupBoxFrontPageAndNewPostsFiltering.Size = New Size(215, 70)
        GroupBoxFrontPageAndNewPostsFiltering.TabIndex = 19
        GroupBoxFrontPageAndNewPostsFiltering.TabStop = False
        GroupBoxFrontPageAndNewPostsFiltering.Text = "Set posts sort criterion and output limit"
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
        ' NumericUpDownFrontPageAndNewPostsLimit
        ' 
        NumericUpDownFrontPageAndNewPostsLimit.Font = New Font("Segoe UI Variable Text Semibold", 8.25F, FontStyle.Bold, GraphicsUnit.Point)
        NumericUpDownFrontPageAndNewPostsLimit.Location = New Point(130, 41)
        NumericUpDownFrontPageAndNewPostsLimit.Maximum = New Decimal(New Integer() {10000, 0, 0, 0})
        NumericUpDownFrontPageAndNewPostsLimit.Minimum = New Decimal(New Integer() {1, 0, 0, 0})
        NumericUpDownFrontPageAndNewPostsLimit.Name = "NumericUpDownFrontPageAndNewPostsLimit"
        NumericUpDownFrontPageAndNewPostsLimit.ReadOnly = True
        NumericUpDownFrontPageAndNewPostsLimit.Size = New Size(79, 22)
        NumericUpDownFrontPageAndNewPostsLimit.TabIndex = 17
        NumericUpDownFrontPageAndNewPostsLimit.Value = New Decimal(New Integer() {100, 0, 0, 0})
        ' 
        ' ButtonGetFrontPageAndNewPosts
        ' 
        ButtonGetFrontPageAndNewPosts.FlatStyle = FlatStyle.Popup
        ButtonGetFrontPageAndNewPosts.Font = New Font("Segoe UI Variable Display", 9.0F, FontStyle.Regular, GraphicsUnit.Point)
        ButtonGetFrontPageAndNewPosts.ForeColor = Color.Black
        ButtonGetFrontPageAndNewPosts.Location = New Point(157, 163)
        ButtonGetFrontPageAndNewPosts.Name = "ButtonGetFrontPageAndNewPosts"
        ButtonGetFrontPageAndNewPosts.Size = New Size(62, 24)
        ButtonGetFrontPageAndNewPosts.TabIndex = 17
        ButtonGetFrontPageAndNewPosts.Text = "&Get"
        ButtonGetFrontPageAndNewPosts.UseVisualStyleBackColor = True
        ' 
        ' GroupBoxCommunityDataFiltering
        ' 
        GroupBoxCommunityDataFiltering.Controls.Add(LabelCommunityPostsLimit)
        GroupBoxCommunityDataFiltering.Controls.Add(LabelCommunityPostsListing)
        GroupBoxCommunityDataFiltering.Controls.Add(NumericUpDownCommunityPostsLimit)
        GroupBoxCommunityDataFiltering.Controls.Add(ComboBoxCommunityPostsListing)
        GroupBoxCommunityDataFiltering.Font = New Font("Segoe UI Variable Display", 8.25F, FontStyle.Underline, GraphicsUnit.Point)
        GroupBoxCommunityDataFiltering.Location = New Point(3, 81)
        GroupBoxCommunityDataFiltering.Name = "GroupBoxCommunityDataFiltering"
        GroupBoxCommunityDataFiltering.Size = New Size(215, 70)
        GroupBoxCommunityDataFiltering.TabIndex = 11
        GroupBoxCommunityDataFiltering.TabStop = False
        GroupBoxCommunityDataFiltering.Text = "Set posts sort criterion and output limit"
        ' 
        ' LabelCommunityPostsLimit
        ' 
        LabelCommunityPostsLimit.AutoSize = True
        LabelCommunityPostsLimit.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        LabelCommunityPostsLimit.Location = New Point(126, 23)
        LabelCommunityPostsLimit.Name = "LabelCommunityPostsLimit"
        LabelCommunityPostsLimit.Size = New Size(75, 15)
        LabelCommunityPostsLimit.TabIndex = 19
        LabelCommunityPostsLimit.Text = "Limit posts to:"
        ' 
        ' LabelCommunityPostsListing
        ' 
        LabelCommunityPostsListing.AutoSize = True
        LabelCommunityPostsListing.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        LabelCommunityPostsListing.Location = New Point(4, 22)
        LabelCommunityPostsListing.Name = "LabelCommunityPostsListing"
        LabelCommunityPostsListing.Size = New Size(72, 15)
        LabelCommunityPostsListing.TabIndex = 18
        LabelCommunityPostsListing.Text = "Sort posts by:"
        ' 
        ' NumericUpDownCommunityPostsLimit
        ' 
        NumericUpDownCommunityPostsLimit.Enabled = False
        NumericUpDownCommunityPostsLimit.Font = New Font("Segoe UI Variable Display Semib", 8.25F, FontStyle.Bold, GraphicsUnit.Point)
        NumericUpDownCommunityPostsLimit.Location = New Point(130, 41)
        NumericUpDownCommunityPostsLimit.Maximum = New Decimal(New Integer() {10000, 0, 0, 0})
        NumericUpDownCommunityPostsLimit.Minimum = New Decimal(New Integer() {1, 0, 0, 0})
        NumericUpDownCommunityPostsLimit.Name = "NumericUpDownCommunityPostsLimit"
        NumericUpDownCommunityPostsLimit.ReadOnly = True
        NumericUpDownCommunityPostsLimit.Size = New Size(79, 22)
        NumericUpDownCommunityPostsLimit.TabIndex = 17
        NumericUpDownCommunityPostsLimit.Value = New Decimal(New Integer() {100, 0, 0, 0})
        ' 
        ' ButtonGetCommunityData
        ' 
        ButtonGetCommunityData.FlatAppearance.BorderSize = 0
        ButtonGetCommunityData.FlatStyle = FlatStyle.Popup
        ButtonGetCommunityData.Font = New Font("Segoe UI Variable Display", 9.0F, FontStyle.Regular, GraphicsUnit.Point)
        ButtonGetCommunityData.ForeColor = Color.Black
        ButtonGetCommunityData.Location = New Point(157, 163)
        ButtonGetCommunityData.Name = "ButtonGetCommunityData"
        ButtonGetCommunityData.Size = New Size(62, 24)
        ButtonGetCommunityData.TabIndex = 6
        ButtonGetCommunityData.Text = "&Get"
        ButtonGetCommunityData.UseVisualStyleBackColor = True
        ' 
        ' GroupBoxCommunityData
        ' 
        GroupBoxCommunityData.BackColor = Color.Transparent
        GroupBoxCommunityData.ContextMenuStrip = ContextMenuStripRightClick
        GroupBoxCommunityData.Controls.Add(RadioButtonCommunityProfile)
        GroupBoxCommunityData.Controls.Add(RadioButtonCommunityPosts)
        GroupBoxCommunityData.FlatStyle = FlatStyle.Flat
        GroupBoxCommunityData.Font = New Font("Segoe UI Variable Display", 8.25F, FontStyle.Underline, GraphicsUnit.Point)
        GroupBoxCommunityData.Location = New Point(3, 26)
        GroupBoxCommunityData.Name = "GroupBoxCommunityData"
        GroupBoxCommunityData.Size = New Size(215, 49)
        GroupBoxCommunityData.TabIndex = 9
        GroupBoxCommunityData.TabStop = False
        GroupBoxCommunityData.Text = "Select subreddit data to fetch"
        ' 
        ' GroupBoxUserDataFiltering
        ' 
        GroupBoxUserDataFiltering.Controls.Add(LabelUserDataLimit)
        GroupBoxUserDataFiltering.Controls.Add(LabelUserPostsListing)
        GroupBoxUserDataFiltering.Controls.Add(NumericUpDownUserDataLimit)
        GroupBoxUserDataFiltering.Controls.Add(ComboBoxUserDataListing)
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
        NumericUpDownUserDataLimit.Maximum = New Decimal(New Integer() {10000, 0, 0, 0})
        NumericUpDownUserDataLimit.Minimum = New Decimal(New Integer() {1, 0, 0, 0})
        NumericUpDownUserDataLimit.Name = "NumericUpDownUserDataLimit"
        NumericUpDownUserDataLimit.ReadOnly = True
        NumericUpDownUserDataLimit.Size = New Size(79, 22)
        NumericUpDownUserDataLimit.TabIndex = 17
        NumericUpDownUserDataLimit.Value = New Decimal(New Integer() {100, 0, 0, 0})
        ' 
        ' ButtonGetUserData
        ' 
        ButtonGetUserData.FlatStyle = FlatStyle.Popup
        ButtonGetUserData.Font = New Font("Segoe UI Variable Display", 9.0F, FontStyle.Regular, GraphicsUnit.Point)
        ButtonGetUserData.ForeColor = Color.Black
        ButtonGetUserData.Location = New Point(157, 163)
        ButtonGetUserData.Name = "ButtonGetUserData"
        ButtonGetUserData.Size = New Size(62, 24)
        ButtonGetUserData.TabIndex = 4
        ButtonGetUserData.Text = "&Get"
        ButtonGetUserData.UseVisualStyleBackColor = True
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
        TreeView1.BorderStyle = BorderStyle.FixedSingle
        TreeView1.HotTracking = True
        TreeView1.Indent = 10
        TreeView1.Location = New Point(12, 12)
        TreeView1.Name = "TreeView1"
        TreeNode1.Name = "childUser"
        TreeNode1.Text = "User"
        TreeNode2.Name = "childCommunity"
        TreeNode2.Text = "Community"
        TreeNode3.Name = "subchildSearch"
        TreeNode3.Text = "Search"
        TreeNode4.Name = "subchildListings"
        TreeNode4.Text = "Listings"
        TreeNode5.Name = "subchildFrontPageAndNew"
        TreeNode5.Text = "Front-Page/New"
        TreeNode6.Name = "childPosts"
        TreeNode6.Text = "Posts"
        TreeNode7.Name = "MainRoot"
        TreeNode7.Text = "Username"
        TreeView1.Nodes.AddRange(New TreeNode() {TreeNode7})
        TreeView1.ShowNodeToolTips = True
        TreeView1.Size = New Size(129, 186)
        TreeView1.TabIndex = 17
        ' 
        ' PanelUserData
        ' 
        PanelUserData.Controls.Add(ButtonGetUserData)
        PanelUserData.Controls.Add(PanelUserDataHeader)
        PanelUserData.Controls.Add(GroupBoxUserData)
        PanelUserData.Controls.Add(TextBoxUsername)
        PanelUserData.Controls.Add(GroupBoxUserDataFiltering)
        PanelUserData.Location = New Point(150, 12)
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
        Label1.Font = New Font("Segoe UI Variable Display Semib", 9.0F, FontStyle.Bold, GraphicsUnit.Point)
        Label1.ForeColor = Color.Black
        Label1.Location = New Point(75, 0)
        Label1.Name = "Label1"
        Label1.Size = New Size(59, 16)
        Label1.TabIndex = 29
        Label1.Text = "User Data"
        ' 
        ' PanelCommunityData
        ' 
        PanelCommunityData.BackColor = Color.Transparent
        PanelCommunityData.Controls.Add(ButtonGetCommunityData)
        PanelCommunityData.Controls.Add(PanelCommunityDataHeader)
        PanelCommunityData.Controls.Add(TextBoxCommunity)
        PanelCommunityData.Controls.Add(GroupBoxCommunityDataFiltering)
        PanelCommunityData.Controls.Add(GroupBoxCommunityData)
        PanelCommunityData.Location = New Point(150, 12)
        PanelCommunityData.Name = "PanelCommunityData"
        PanelCommunityData.Size = New Size(221, 188)
        PanelCommunityData.TabIndex = 21
        PanelCommunityData.Visible = False
        ' 
        ' PanelCommunityDataHeader
        ' 
        PanelCommunityDataHeader.BackColor = Color.Transparent
        PanelCommunityDataHeader.BorderStyle = BorderStyle.FixedSingle
        PanelCommunityDataHeader.Controls.Add(Label2)
        PanelCommunityDataHeader.Enabled = False
        PanelCommunityDataHeader.Location = New Point(3, 0)
        PanelCommunityDataHeader.Name = "PanelCommunityDataHeader"
        PanelCommunityDataHeader.Size = New Size(215, 20)
        PanelCommunityDataHeader.TabIndex = 30
        ' 
        ' Label2
        ' 
        Label2.AutoSize = True
        Label2.BackColor = Color.Transparent
        Label2.Font = New Font("Segoe UI Variable Display Semib", 9.0F, FontStyle.Bold, GraphicsUnit.Point)
        Label2.ForeColor = Color.Black
        Label2.Location = New Point(55, 0)
        Label2.Name = "Label2"
        Label2.Size = New Size(101, 16)
        Label2.TabIndex = 29
        Label2.Text = "Community Data"
        ' 
        ' PanelFrontPageAndNew
        ' 
        PanelFrontPageAndNew.Controls.Add(GroupBoxFrontPageAndNewPosts)
        PanelFrontPageAndNew.Controls.Add(ButtonGetFrontPageAndNewPosts)
        PanelFrontPageAndNew.Controls.Add(PanelFrontPageAndNewHeader)
        PanelFrontPageAndNew.Controls.Add(GroupBoxFrontPageAndNewPostsFiltering)
        PanelFrontPageAndNew.Location = New Point(150, 12)
        PanelFrontPageAndNew.Name = "PanelFrontPageAndNew"
        PanelFrontPageAndNew.Size = New Size(221, 188)
        PanelFrontPageAndNew.TabIndex = 25
        PanelFrontPageAndNew.Visible = False
        ' 
        ' GroupBoxFrontPageAndNewPosts
        ' 
        GroupBoxFrontPageAndNewPosts.BackColor = Color.Transparent
        GroupBoxFrontPageAndNewPosts.ContextMenuStrip = ContextMenuStripRightClick
        GroupBoxFrontPageAndNewPosts.Controls.Add(RadioButtonNewPosts)
        GroupBoxFrontPageAndNewPosts.Controls.Add(RadioButtonFrontPagePosts)
        GroupBoxFrontPageAndNewPosts.FlatStyle = FlatStyle.Flat
        GroupBoxFrontPageAndNewPosts.Font = New Font("Segoe UI Variable Display", 8.25F, FontStyle.Underline, GraphicsUnit.Point)
        GroupBoxFrontPageAndNewPosts.Location = New Point(3, 26)
        GroupBoxFrontPageAndNewPosts.Name = "GroupBoxFrontPageAndNewPosts"
        GroupBoxFrontPageAndNewPosts.Size = New Size(215, 49)
        GroupBoxFrontPageAndNewPosts.TabIndex = 33
        GroupBoxFrontPageAndNewPosts.TabStop = False
        GroupBoxFrontPageAndNewPosts.Text = "Select source to get posts from"
        ' 
        ' RadioButtonNewPosts
        ' 
        RadioButtonNewPosts.AutoSize = True
        RadioButtonNewPosts.Checked = True
        RadioButtonNewPosts.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        RadioButtonNewPosts.Location = New Point(6, 23)
        RadioButtonNewPosts.Name = "RadioButtonNewPosts"
        RadioButtonNewPosts.Size = New Size(47, 19)
        RadioButtonNewPosts.TabIndex = 5
        RadioButtonNewPosts.TabStop = True
        RadioButtonNewPosts.Text = "New"
        RadioButtonNewPosts.UseVisualStyleBackColor = True
        ' 
        ' RadioButtonFrontPagePosts
        ' 
        RadioButtonFrontPagePosts.AutoSize = True
        RadioButtonFrontPagePosts.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        RadioButtonFrontPagePosts.Location = New Point(61, 23)
        RadioButtonFrontPagePosts.Name = "RadioButtonFrontPagePosts"
        RadioButtonFrontPagePosts.Size = New Size(78, 19)
        RadioButtonFrontPagePosts.TabIndex = 6
        RadioButtonFrontPagePosts.Text = "Front-Page"
        RadioButtonFrontPagePosts.UseVisualStyleBackColor = True
        ' 
        ' PanelFrontPageAndNewHeader
        ' 
        PanelFrontPageAndNewHeader.BackColor = Color.Transparent
        PanelFrontPageAndNewHeader.BorderStyle = BorderStyle.FixedSingle
        PanelFrontPageAndNewHeader.Controls.Add(Label5)
        PanelFrontPageAndNewHeader.Enabled = False
        PanelFrontPageAndNewHeader.Location = New Point(3, 0)
        PanelFrontPageAndNewHeader.Name = "PanelFrontPageAndNewHeader"
        PanelFrontPageAndNewHeader.Size = New Size(215, 20)
        PanelFrontPageAndNewHeader.TabIndex = 32
        ' 
        ' Label5
        ' 
        Label5.AutoSize = True
        Label5.BackColor = Color.Transparent
        Label5.Font = New Font("Segoe UI Variable Display Semib", 9.0F, FontStyle.Bold, GraphicsUnit.Point)
        Label5.ForeColor = Color.Black
        Label5.Location = New Point(40, 0)
        Label5.Name = "Label5"
        Label5.Size = New Size(129, 16)
        Label5.TabIndex = 29
        Label5.Text = "Front-Page/New Posts"
        ' 
        ' PanelPostListings
        ' 
        PanelPostListings.Controls.Add(ButtonGetListingPosts)
        PanelPostListings.Controls.Add(PanelPostListingsDataHeader)
        PanelPostListings.Controls.Add(GroupBoxPostListingsFiltering)
        PanelPostListings.Controls.Add(GroupBoxPostListings)
        PanelPostListings.Location = New Point(150, 12)
        PanelPostListings.Name = "PanelPostListings"
        PanelPostListings.Size = New Size(221, 188)
        PanelPostListings.TabIndex = 26
        PanelPostListings.Visible = False
        ' 
        ' ButtonGetListingPosts
        ' 
        ButtonGetListingPosts.FlatStyle = FlatStyle.Popup
        ButtonGetListingPosts.Font = New Font("Segoe UI Variable Display", 9.0F, FontStyle.Regular, GraphicsUnit.Point)
        ButtonGetListingPosts.ForeColor = Color.Black
        ButtonGetListingPosts.Location = New Point(157, 162)
        ButtonGetListingPosts.Name = "ButtonGetListingPosts"
        ButtonGetListingPosts.Size = New Size(62, 24)
        ButtonGetListingPosts.TabIndex = 31
        ButtonGetListingPosts.Text = "&Get"
        ButtonGetListingPosts.UseVisualStyleBackColor = True
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
        Label3.Font = New Font("Segoe UI Variable Display Semib", 9.0F, FontStyle.Bold, GraphicsUnit.Point)
        Label3.ForeColor = Color.Black
        Label3.Location = New Point(67, 0)
        Label3.Name = "Label3"
        Label3.Size = New Size(75, 16)
        Label3.TabIndex = 29
        Label3.Text = "Listing Posts"
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
        NumericUpDownPostListingsLimit.Maximum = New Decimal(New Integer() {10000, 0, 0, 0})
        NumericUpDownPostListingsLimit.Minimum = New Decimal(New Integer() {1, 0, 0, 0})
        NumericUpDownPostListingsLimit.Name = "NumericUpDownPostListingsLimit"
        NumericUpDownPostListingsLimit.ReadOnly = True
        NumericUpDownPostListingsLimit.Size = New Size(79, 22)
        NumericUpDownPostListingsLimit.TabIndex = 17
        NumericUpDownPostListingsLimit.Value = New Decimal(New Integer() {100, 0, 0, 0})
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
        GroupBoxPostListings.Text = "Get posts from selected listing"
        ' 
        ' PanelSearch
        ' 
        PanelSearch.Controls.Add(GroupBoxSearchData)
        PanelSearch.Controls.Add(ButtonSearch)
        PanelSearch.Controls.Add(Panel1)
        PanelSearch.Controls.Add(TextBoxQuery)
        PanelSearch.Controls.Add(GroupBoxSearchResultsFiltering)
        PanelSearch.Location = New Point(150, 12)
        PanelSearch.Name = "PanelSearch"
        PanelSearch.Size = New Size(221, 188)
        PanelSearch.TabIndex = 27
        PanelSearch.Visible = False
        ' 
        ' GroupBoxSearchData
        ' 
        GroupBoxSearchData.BackColor = Color.Transparent
        GroupBoxSearchData.ContextMenuStrip = ContextMenuStripRightClick
        GroupBoxSearchData.Controls.Add(RadioButtonSearchCommunities)
        GroupBoxSearchData.Controls.Add(RadioButtonSearchUsers)
        GroupBoxSearchData.Controls.Add(RadioButtonSearchPosts)
        GroupBoxSearchData.FlatStyle = FlatStyle.Flat
        GroupBoxSearchData.Font = New Font("Segoe UI Variable Display", 8.25F, FontStyle.Underline, GraphicsUnit.Point)
        GroupBoxSearchData.Location = New Point(3, 26)
        GroupBoxSearchData.Name = "GroupBoxSearchData"
        GroupBoxSearchData.Size = New Size(215, 49)
        GroupBoxSearchData.TabIndex = 32
        GroupBoxSearchData.TabStop = False
        GroupBoxSearchData.Text = "Select an entity to search for"
        ' 
        ' RadioButtonSearchCommunities
        ' 
        RadioButtonSearchCommunities.AutoSize = True
        RadioButtonSearchCommunities.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        RadioButtonSearchCommunities.Location = New Point(115, 23)
        RadioButtonSearchCommunities.Name = "RadioButtonSearchCommunities"
        RadioButtonSearchCommunities.Size = New Size(89, 19)
        RadioButtonSearchCommunities.TabIndex = 7
        RadioButtonSearchCommunities.Text = "Communities"
        RadioButtonSearchCommunities.UseVisualStyleBackColor = True
        ' 
        ' RadioButtonSearchUsers
        ' 
        RadioButtonSearchUsers.AutoSize = True
        RadioButtonSearchUsers.Checked = True
        RadioButtonSearchUsers.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        RadioButtonSearchUsers.Location = New Point(6, 23)
        RadioButtonSearchUsers.Name = "RadioButtonSearchUsers"
        RadioButtonSearchUsers.Size = New Size(53, 19)
        RadioButtonSearchUsers.TabIndex = 5
        RadioButtonSearchUsers.TabStop = True
        RadioButtonSearchUsers.Text = "Users"
        RadioButtonSearchUsers.UseVisualStyleBackColor = True
        ' 
        ' RadioButtonSearchPosts
        ' 
        RadioButtonSearchPosts.AutoSize = True
        RadioButtonSearchPosts.Font = New Font("Segoe UI Variable Text", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        RadioButtonSearchPosts.Location = New Point(61, 23)
        RadioButtonSearchPosts.Name = "RadioButtonSearchPosts"
        RadioButtonSearchPosts.Size = New Size(51, 19)
        RadioButtonSearchPosts.TabIndex = 6
        RadioButtonSearchPosts.Text = "Posts"
        RadioButtonSearchPosts.UseVisualStyleBackColor = True
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
        Label4.Font = New Font("Segoe UI Variable Display Semib", 9.0F, FontStyle.Bold, GraphicsUnit.Point)
        Label4.ForeColor = Color.Black
        Label4.Location = New Point(83, 0)
        Label4.Name = "Label4"
        Label4.Size = New Size(44, 16)
        Label4.TabIndex = 29
        Label4.Text = "Search"
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
        ' PanelHome
        ' 
        PanelHome.Controls.Add(LabelProgramLastName)
        PanelHome.Controls.Add(LabelProgramFirstName)
        PanelHome.Controls.Add(Panel3)
        PanelHome.Location = New Point(150, 12)
        PanelHome.Name = "PanelHome"
        PanelHome.Size = New Size(221, 188)
        PanelHome.TabIndex = 28
        PanelHome.Visible = False
        ' 
        ' LabelProgramLastName
        ' 
        LabelProgramLastName.AutoSize = True
        LabelProgramLastName.BackColor = Color.Transparent
        LabelProgramLastName.Font = New Font("Segoe UI Variable Display", 18.0F, FontStyle.Underline, GraphicsUnit.Point)
        LabelProgramLastName.ForeColor = Color.FromArgb(CByte(255), CByte(87), CByte(0))
        LabelProgramLastName.Location = New Point(107, 78)
        LabelProgramLastName.Name = "LabelProgramLastName"
        LabelProgramLastName.Size = New Size(81, 32)
        LabelProgramLastName.TabIndex = 35
        LabelProgramLastName.Text = "Karma"
        ' 
        ' LabelProgramFirstName
        ' 
        LabelProgramFirstName.AutoSize = True
        LabelProgramFirstName.Font = New Font("Segoe UI Variable Display", 18.0F, FontStyle.Bold Or FontStyle.Underline, GraphicsUnit.Point)
        LabelProgramFirstName.ForeColor = SystemColors.ControlText
        LabelProgramFirstName.Location = New Point(39, 78)
        LabelProgramFirstName.Name = "LabelProgramFirstName"
        LabelProgramFirstName.Size = New Size(76, 32)
        LabelProgramFirstName.TabIndex = 34
        LabelProgramFirstName.Text = "Knew"
        ' 
        ' Panel3
        ' 
        Panel3.BackColor = Color.Transparent
        Panel3.BorderStyle = BorderStyle.FixedSingle
        Panel3.Controls.Add(Label6)
        Panel3.Enabled = False
        Panel3.Location = New Point(3, 0)
        Panel3.Name = "Panel3"
        Panel3.Size = New Size(215, 20)
        Panel3.TabIndex = 32
        ' 
        ' Label6
        ' 
        Label6.AutoSize = True
        Label6.BackColor = Color.Transparent
        Label6.Font = New Font("Segoe UI Variable Display Semib", 9.0F, FontStyle.Bold, GraphicsUnit.Point)
        Label6.ForeColor = Color.Black
        Label6.Location = New Point(84, 0)
        Label6.Name = "Label6"
        Label6.Size = New Size(40, 16)
        Label6.TabIndex = 29
        Label6.Text = "Home"
        ' 
        ' MainWindow
        ' 
        AccessibleRole = AccessibleRole.Window
        AutoScaleDimensions = New SizeF(7.0F, 16.0F)
        AutoScaleMode = AutoScaleMode.Font
        BackColor = Color.White
        ClientSize = New Size(384, 216)
        ContextMenuStrip = ContextMenuStripRightClick
        Controls.Add(PanelHome)
        Controls.Add(PanelCommunityData)
        Controls.Add(PanelSearch)
        Controls.Add(PanelPostListings)
        Controls.Add(PanelFrontPageAndNew)
        Controls.Add(PanelUserData)
        Controls.Add(TreeView1)
        Font = New Font("Segoe UI Variable Display", 9.0F, FontStyle.Regular, GraphicsUnit.Point)
        ForeColor = Color.Black
        FormBorderStyle = FormBorderStyle.FixedDialog
        HelpButton = True
        Icon = CType(resources.GetObject("$this.Icon"), Icon)
        MaximizeBox = False
        MinimizeBox = False
        Name = "MainWindow"
        StartPosition = FormStartPosition.CenterScreen
        ContextMenuStripRightClick.ResumeLayout(False)
        GroupBoxSearchResultsFiltering.ResumeLayout(False)
        GroupBoxSearchResultsFiltering.PerformLayout()
        CType(NumericUpDownSearchResultLimit, ComponentModel.ISupportInitialize).EndInit()
        GroupBoxFrontPageAndNewPostsFiltering.ResumeLayout(False)
        GroupBoxFrontPageAndNewPostsFiltering.PerformLayout()
        CType(NumericUpDownFrontPageAndNewPostsLimit, ComponentModel.ISupportInitialize).EndInit()
        GroupBoxCommunityDataFiltering.ResumeLayout(False)
        GroupBoxCommunityDataFiltering.PerformLayout()
        CType(NumericUpDownCommunityPostsLimit, ComponentModel.ISupportInitialize).EndInit()
        GroupBoxCommunityData.ResumeLayout(False)
        GroupBoxCommunityData.PerformLayout()
        GroupBoxUserDataFiltering.ResumeLayout(False)
        GroupBoxUserDataFiltering.PerformLayout()
        CType(NumericUpDownUserDataLimit, ComponentModel.ISupportInitialize).EndInit()
        GroupBoxUserData.ResumeLayout(False)
        GroupBoxUserData.PerformLayout()
        PanelUserData.ResumeLayout(False)
        PanelUserData.PerformLayout()
        PanelUserDataHeader.ResumeLayout(False)
        PanelUserDataHeader.PerformLayout()
        PanelCommunityData.ResumeLayout(False)
        PanelCommunityData.PerformLayout()
        PanelCommunityDataHeader.ResumeLayout(False)
        PanelCommunityDataHeader.PerformLayout()
        PanelFrontPageAndNew.ResumeLayout(False)
        GroupBoxFrontPageAndNewPosts.ResumeLayout(False)
        GroupBoxFrontPageAndNewPosts.PerformLayout()
        PanelFrontPageAndNewHeader.ResumeLayout(False)
        PanelFrontPageAndNewHeader.PerformLayout()
        PanelPostListings.ResumeLayout(False)
        PanelPostListingsDataHeader.ResumeLayout(False)
        PanelPostListingsDataHeader.PerformLayout()
        GroupBoxPostListingsFiltering.ResumeLayout(False)
        GroupBoxPostListingsFiltering.PerformLayout()
        CType(NumericUpDownPostListingsLimit, ComponentModel.ISupportInitialize).EndInit()
        GroupBoxPostListings.ResumeLayout(False)
        GroupBoxPostListings.PerformLayout()
        PanelSearch.ResumeLayout(False)
        PanelSearch.PerformLayout()
        GroupBoxSearchData.ResumeLayout(False)
        GroupBoxSearchData.PerformLayout()
        Panel1.ResumeLayout(False)
        Panel1.PerformLayout()
        PanelHome.ResumeLayout(False)
        PanelHome.PerformLayout()
        Panel3.ResumeLayout(False)
        Panel3.PerformLayout()
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
    Friend WithEvents ButtonGetUserData As Button
    Friend WithEvents TextBoxCommunity As TextBox
    Friend WithEvents ButtonGetCommunityData As Button
    Friend WithEvents RadioButtonUserPosts As RadioButton
    Friend WithEvents RadioButtonUserProfile As RadioButton
    Friend WithEvents RadioButtonUserComments As RadioButton
    Friend WithEvents GroupBoxUserData As GroupBox
    Friend WithEvents GroupBoxCommunityData As GroupBox
    Friend WithEvents RadioButtonCommunityProfile As RadioButton
    Friend WithEvents RadioButtonCommunityPosts As RadioButton
    Friend WithEvents GroupBoxUserDataFiltering As GroupBox
    Friend WithEvents ComboBoxUserDataListing As ComboBox
    Friend WithEvents NumericUpDownUserDataLimit As NumericUpDown
    Friend WithEvents LabelUserDataLimit As Label
    Friend WithEvents LabelUserPostsListing As Label
    Friend WithEvents GroupBoxSearchResultsFiltering As GroupBox
    Friend WithEvents LabelSearchResultsLimit As Label
    Friend WithEvents LabelSearchResultsListing As Label
    Friend WithEvents NumericUpDownSearchResultLimit As NumericUpDown
    Friend WithEvents ComboBoxSearchResultListing As ComboBox
    Friend WithEvents GroupBoxCommunityDataFiltering As GroupBox
    Friend WithEvents LabelCommunityPostsLimit As Label
    Friend WithEvents LabelCommunityPostsListing As Label
    Friend WithEvents NumericUpDownCommunityPostsLimit As NumericUpDown
    Friend WithEvents ComboBoxCommunityPostsListing As ComboBox
    Friend WithEvents NumericUpDown2 As NumericUpDown
    Friend WithEvents ButtonGetFrontPageAndNewPosts As Button
    Friend WithEvents GroupBoxFrontPageAndNewPostsFiltering As GroupBox
    Friend WithEvents LabelFrontPageDataLimit As Label
    Friend WithEvents LabelFrontPageDataListing As Label
    Friend WithEvents NumericUpDownFrontPageAndNewPostsLimit As NumericUpDown
    Friend WithEvents ComboBoxFrontPageAndNewPostsListing As ComboBox
    Friend WithEvents TreeView1 As TreeView
    Friend WithEvents PanelUserData As Panel
    Friend WithEvents PanelCommunityData As Panel
    Friend WithEvents PanelFrontPageAndNew As Panel
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
    Friend WithEvents PanelSearch As Panel
    Friend WithEvents GroupBoxUser As GroupBox
    Friend WithEvents DarkModeEnableToolStripMenuItem As ToolStripMenuItem
    Friend WithEvents DarkModeDisableToolStripMenuItem As ToolStripMenuItem
    Friend WithEvents PanelUserDataHeader As Panel
    Friend WithEvents Label1 As Label
    Friend WithEvents PanelCommunityDataHeader As Panel
    Friend WithEvents Label2 As Label
    Friend WithEvents PanelPostListingsDataHeader As Panel
    Friend WithEvents Label3 As Label
    Friend WithEvents Panel1 As Panel
    Friend WithEvents Label4 As Label
    Friend WithEvents PanelFrontPageAndNewHeader As Panel
    Friend WithEvents Label5 As Label
    Friend WithEvents NotifyIcon1 As NotifyIcon
    Friend WithEvents ButtonGetListingPosts As Button
    Friend WithEvents GroupBoxSearchData As GroupBox
    Friend WithEvents RadioButtonSearchCommunities As RadioButton
    Friend WithEvents RadioButtonSearchUsers As RadioButton
    Friend WithEvents RadioButtonSearchPosts As RadioButton
    Friend WithEvents GroupBoxFrontPageAndNewPosts As GroupBox
    Friend WithEvents RadioButtonNewPosts As RadioButton
    Friend WithEvents RadioButtonFrontPagePosts As RadioButton
    Friend WithEvents PanelHome As Panel
    Friend WithEvents Panel3 As Panel
    Friend WithEvents Label6 As Label
    Friend WithEvents LabelProgramFirstName As Label
    Friend WithEvents LabelProgramLastName As Label
End Class
