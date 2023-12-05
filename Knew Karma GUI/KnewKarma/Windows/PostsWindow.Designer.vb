<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()>
Partial Class PostsWindow
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
        Dim DataGridViewCellStyle1 As DataGridViewCellStyle = New DataGridViewCellStyle()
        Dim resources As ComponentModel.ComponentResourceManager = New ComponentModel.ComponentResourceManager(GetType(PostsWindow))
        DataGridViewPosts = New DataGridView()
        postAuthor = New DataGridViewTextBoxColumn()
        postTitle = New DataGridViewTextBoxColumn()
        postText = New DataGridViewTextBoxColumn()
        postID = New DataGridViewTextBoxColumn()
        postSubreddit = New DataGridViewTextBoxColumn()
        postSubredditType = New DataGridViewTextBoxColumn()
        postUpvotes = New DataGridViewTextBoxColumn()
        postUpvoteRatio = New DataGridViewTextBoxColumn()
        postDownvotes = New DataGridViewTextBoxColumn()
        postThumbnail = New DataGridViewTextBoxColumn()
        postScore = New DataGridViewTextBoxColumn()
        postComments = New DataGridViewTextBoxColumn()
        postAwards = New DataGridViewTextBoxColumn()
        postDomain = New DataGridViewTextBoxColumn()
        postPermalink = New DataGridViewTextBoxColumn()
        postLinkFlairText = New DataGridViewTextBoxColumn()
        postGilded = New DataGridViewTextBoxColumn()
        postIsNSFW = New DataGridViewTextBoxColumn()
        postIsCrosspostable = New DataGridViewTextBoxColumn()
        postIsEdited = New DataGridViewTextBoxColumn()
        postIsRobotIndexable = New DataGridViewTextBoxColumn()
        postIsStickied = New DataGridViewTextBoxColumn()
        postIsLocked = New DataGridViewTextBoxColumn()
        postIsOriginalContent = New DataGridViewTextBoxColumn()
        postIsRedditMediaDomain = New DataGridViewTextBoxColumn()
        postIsArchived = New DataGridViewTextBoxColumn()
        postIsQuarantined = New DataGridViewTextBoxColumn()
        postCreatedOn = New DataGridViewTextBoxColumn()
        CType(DataGridViewPosts, ComponentModel.ISupportInitialize).BeginInit()
        SuspendLayout()
        ' 
        ' DataGridViewPosts
        ' 
        DataGridViewPosts.AllowUserToAddRows = False
        DataGridViewPosts.AllowUserToDeleteRows = False
        DataGridViewCellStyle1.BackColor = Color.White
        DataGridViewPosts.AlternatingRowsDefaultCellStyle = DataGridViewCellStyle1
        DataGridViewPosts.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill
        DataGridViewPosts.AutoSizeRowsMode = DataGridViewAutoSizeRowsMode.AllCells
        DataGridViewPosts.BackgroundColor = Color.White
        DataGridViewPosts.BorderStyle = BorderStyle.None
        DataGridViewPosts.CellBorderStyle = DataGridViewCellBorderStyle.Raised
        DataGridViewPosts.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize
        DataGridViewPosts.Columns.AddRange(New DataGridViewColumn() {postAuthor, postTitle, postText, postID, postSubreddit, postSubredditType, postUpvotes, postUpvoteRatio, postDownvotes, postThumbnail, postScore, postComments, postAwards, postDomain, postPermalink, postLinkFlairText, postGilded, postIsNSFW, postIsCrosspostable, postIsEdited, postIsRobotIndexable, postIsStickied, postIsLocked, postIsOriginalContent, postIsRedditMediaDomain, postIsArchived, postIsQuarantined, postCreatedOn})
        DataGridViewPosts.Dock = DockStyle.Fill
        DataGridViewPosts.EditMode = DataGridViewEditMode.EditProgrammatically
        DataGridViewPosts.Location = New Point(0, 0)
        DataGridViewPosts.Name = "DataGridViewPosts"
        DataGridViewPosts.ReadOnly = True
        DataGridViewPosts.RowHeadersVisible = False
        DataGridViewPosts.RowTemplate.Height = 25
        DataGridViewPosts.Size = New Size(450, 327)
        DataGridViewPosts.TabIndex = 3
        ' 
        ' postAuthor
        ' 
        postAuthor.HeaderText = "Author"
        postAuthor.Name = "postAuthor"
        postAuthor.ReadOnly = True
        ' 
        ' postTitle
        ' 
        postTitle.HeaderText = "Title"
        postTitle.Name = "postTitle"
        postTitle.ReadOnly = True
        ' 
        ' postText
        ' 
        postText.HeaderText = "Text"
        postText.Name = "postText"
        postText.ReadOnly = True
        ' 
        ' postID
        ' 
        postID.HeaderText = "ID"
        postID.Name = "postID"
        postID.ReadOnly = True
        ' 
        ' postSubreddit
        ' 
        postSubreddit.HeaderText = "Subreddit"
        postSubreddit.Name = "postSubreddit"
        postSubreddit.ReadOnly = True
        ' 
        ' postSubredditType
        ' 
        postSubredditType.HeaderText = "Subreddit Type"
        postSubredditType.Name = "postSubredditType"
        postSubredditType.ReadOnly = True
        ' 
        ' postUpvotes
        ' 
        postUpvotes.HeaderText = "Upvotes"
        postUpvotes.Name = "postUpvotes"
        postUpvotes.ReadOnly = True
        ' 
        ' postUpvoteRatio
        ' 
        postUpvoteRatio.HeaderText = "Upvote Ratio"
        postUpvoteRatio.Name = "postUpvoteRatio"
        postUpvoteRatio.ReadOnly = True
        ' 
        ' postDownvotes
        ' 
        postDownvotes.HeaderText = "Downvotes"
        postDownvotes.Name = "postDownvotes"
        postDownvotes.ReadOnly = True
        ' 
        ' postThumbnail
        ' 
        postThumbnail.HeaderText = "Thumbnail"
        postThumbnail.Name = "postThumbnail"
        postThumbnail.ReadOnly = True
        ' 
        ' postScore
        ' 
        postScore.HeaderText = "Score"
        postScore.Name = "postScore"
        postScore.ReadOnly = True
        ' 
        ' postComments
        ' 
        postComments.HeaderText = "Comments"
        postComments.Name = "postComments"
        postComments.ReadOnly = True
        ' 
        ' postAwards
        ' 
        postAwards.HeaderText = "Awards"
        postAwards.Name = "postAwards"
        postAwards.ReadOnly = True
        ' 
        ' postDomain
        ' 
        postDomain.HeaderText = "Domain"
        postDomain.Name = "postDomain"
        postDomain.ReadOnly = True
        ' 
        ' postPermalink
        ' 
        postPermalink.HeaderText = "Permalink"
        postPermalink.Name = "postPermalink"
        postPermalink.ReadOnly = True
        ' 
        ' postLinkFlairText
        ' 
        postLinkFlairText.HeaderText = "Link Flair Text"
        postLinkFlairText.Name = "postLinkFlairText"
        postLinkFlairText.ReadOnly = True
        ' 
        ' postGilded
        ' 
        postGilded.HeaderText = "Gilded"
        postGilded.Name = "postGilded"
        postGilded.ReadOnly = True
        ' 
        ' postIsNSFW
        ' 
        postIsNSFW.HeaderText = "Is NSFW"
        postIsNSFW.Name = "postIsNSFW"
        postIsNSFW.ReadOnly = True
        ' 
        ' postIsCrosspostable
        ' 
        postIsCrosspostable.HeaderText = "Is Cross-postable"
        postIsCrosspostable.Name = "postIsCrosspostable"
        postIsCrosspostable.ReadOnly = True
        ' 
        ' postIsEdited
        ' 
        postIsEdited.HeaderText = "Is Edited"
        postIsEdited.Name = "postIsEdited"
        postIsEdited.ReadOnly = True
        ' 
        ' postIsRobotIndexable
        ' 
        postIsRobotIndexable.HeaderText = "Is Robot Indexable"
        postIsRobotIndexable.Name = "postIsRobotIndexable"
        postIsRobotIndexable.ReadOnly = True
        ' 
        ' postIsStickied
        ' 
        postIsStickied.HeaderText = "Is Stickied"
        postIsStickied.Name = "postIsStickied"
        postIsStickied.ReadOnly = True
        ' 
        ' postIsLocked
        ' 
        postIsLocked.HeaderText = "Is Locked"
        postIsLocked.Name = "postIsLocked"
        postIsLocked.ReadOnly = True
        ' 
        ' postIsOriginalContent
        ' 
        postIsOriginalContent.HeaderText = "Is Original Content"
        postIsOriginalContent.Name = "postIsOriginalContent"
        postIsOriginalContent.ReadOnly = True
        ' 
        ' postIsRedditMediaDomain
        ' 
        postIsRedditMediaDomain.HeaderText = "Is Reddit Media Domain"
        postIsRedditMediaDomain.Name = "postIsRedditMediaDomain"
        postIsRedditMediaDomain.ReadOnly = True
        ' 
        ' postIsArchived
        ' 
        postIsArchived.HeaderText = "Is Archived"
        postIsArchived.Name = "postIsArchived"
        postIsArchived.ReadOnly = True
        ' 
        ' postIsQuarantined
        ' 
        postIsQuarantined.HeaderText = "Is Quarantined"
        postIsQuarantined.Name = "postIsQuarantined"
        postIsQuarantined.ReadOnly = True
        ' 
        ' postCreatedOn
        ' 
        postCreatedOn.HeaderText = "Posted On"
        postCreatedOn.Name = "postCreatedOn"
        postCreatedOn.ReadOnly = True
        ' 
        ' PostsWindow
        ' 
        AutoScaleDimensions = New SizeF(7F, 16F)
        AutoScaleMode = AutoScaleMode.Font
        ClientSize = New Size(450, 327)
        Controls.Add(DataGridViewPosts)
        Font = New Font("Segoe UI Variable Text", 9F, FontStyle.Regular, GraphicsUnit.Point)
        Icon = CType(resources.GetObject("$this.Icon"), Icon)
        MinimizeBox = False
        Name = "PostsWindow"
        StartPosition = FormStartPosition.CenterScreen
        Text = "Posts"
        CType(DataGridViewPosts, ComponentModel.ISupportInitialize).EndInit()
        ResumeLayout(False)
    End Sub

    Friend WithEvents DataGridViewPosts As DataGridView
    Friend WithEvents postAuthor As DataGridViewTextBoxColumn
    Friend WithEvents postTitle As DataGridViewTextBoxColumn
    Friend WithEvents postText As DataGridViewTextBoxColumn
    Friend WithEvents postID As DataGridViewTextBoxColumn
    Friend WithEvents postSubreddit As DataGridViewTextBoxColumn
    Friend WithEvents postSubredditType As DataGridViewTextBoxColumn
    Friend WithEvents postUpvotes As DataGridViewTextBoxColumn
    Friend WithEvents postUpvoteRatio As DataGridViewTextBoxColumn
    Friend WithEvents postDownvotes As DataGridViewTextBoxColumn
    Friend WithEvents postThumbnail As DataGridViewTextBoxColumn
    Friend WithEvents postScore As DataGridViewTextBoxColumn
    Friend WithEvents postComments As DataGridViewTextBoxColumn
    Friend WithEvents postAwards As DataGridViewTextBoxColumn
    Friend WithEvents postDomain As DataGridViewTextBoxColumn
    Friend WithEvents postPermalink As DataGridViewTextBoxColumn
    Friend WithEvents postLinkFlairText As DataGridViewTextBoxColumn
    Friend WithEvents postGilded As DataGridViewTextBoxColumn
    Friend WithEvents postIsNSFW As DataGridViewTextBoxColumn
    Friend WithEvents postIsCrosspostable As DataGridViewTextBoxColumn
    Friend WithEvents postIsEdited As DataGridViewTextBoxColumn
    Friend WithEvents postIsRobotIndexable As DataGridViewTextBoxColumn
    Friend WithEvents postIsStickied As DataGridViewTextBoxColumn
    Friend WithEvents postIsLocked As DataGridViewTextBoxColumn
    Friend WithEvents postIsOriginalContent As DataGridViewTextBoxColumn
    Friend WithEvents postIsRedditMediaDomain As DataGridViewTextBoxColumn
    Friend WithEvents postIsArchived As DataGridViewTextBoxColumn
    Friend WithEvents postIsQuarantined As DataGridViewTextBoxColumn
    Friend WithEvents postCreatedOn As DataGridViewTextBoxColumn
End Class
