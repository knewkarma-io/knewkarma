<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class CommentsWindow
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()> _
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
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Dim DataGridViewCellStyle1 As DataGridViewCellStyle = New DataGridViewCellStyle()
        Dim resources As ComponentModel.ComponentResourceManager = New ComponentModel.ComponentResourceManager(GetType(CommentsWindow))
        DataGridViewComments = New DataGridView()
        commentSubreddit = New DataGridViewTextBoxColumn()
        commentSubredditType = New DataGridViewTextBoxColumn()
        commentAuthor = New DataGridViewTextBoxColumn()
        commentAuthorFlairType = New DataGridViewTextBoxColumn()
        commentAuthorIsPremium = New DataGridViewTextBoxColumn()
        commentTitle = New DataGridViewTextBoxColumn()
        commentBody = New DataGridViewTextBoxColumn()
        commentID = New DataGridViewTextBoxColumn()
        commentPermalink = New DataGridViewTextBoxColumn()
        commentUpvotes = New DataGridViewTextBoxColumn()
        commentDownvotes = New DataGridViewTextBoxColumn()
        commentScore = New DataGridViewTextBoxColumn()
        isCommentScoreHidden = New DataGridViewTextBoxColumn()
        commentReplies = New DataGridViewTextBoxColumn()
        commentAwards = New DataGridViewTextBoxColumn()
        commentGilded = New DataGridViewTextBoxColumn()
        commentIsNSFW = New DataGridViewTextBoxColumn()
        commentIsEdited = New DataGridViewTextBoxColumn()
        commentIsStickied = New DataGridViewTextBoxColumn()
        commentIsLocked = New DataGridViewTextBoxColumn()
        commentIsArchived = New DataGridViewTextBoxColumn()
        commentIsQuarantined = New DataGridViewTextBoxColumn()
        commentCreatedAt = New DataGridViewTextBoxColumn()
        CType(DataGridViewComments, ComponentModel.ISupportInitialize).BeginInit()
        SuspendLayout()
        ' 
        ' DataGridViewComments
        ' 
        DataGridViewComments.AllowUserToAddRows = False
        DataGridViewComments.AllowUserToDeleteRows = False
        DataGridViewCellStyle1.BackColor = Color.White
        DataGridViewComments.AlternatingRowsDefaultCellStyle = DataGridViewCellStyle1
        DataGridViewComments.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill
        DataGridViewComments.AutoSizeRowsMode = DataGridViewAutoSizeRowsMode.AllCells
        DataGridViewComments.BackgroundColor = Color.White
        DataGridViewComments.BorderStyle = BorderStyle.Fixed3D
        DataGridViewComments.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize
        DataGridViewComments.Columns.AddRange(New DataGridViewColumn() {commentSubreddit, commentSubredditType, commentAuthor, commentAuthorFlairType, commentAuthorIsPremium, commentTitle, commentBody, commentID, commentPermalink, commentUpvotes, commentDownvotes, commentScore, isCommentScoreHidden, commentReplies, commentAwards, commentGilded, commentIsNSFW, commentIsEdited, commentIsStickied, commentIsLocked, commentIsArchived, commentIsQuarantined, commentCreatedAt})
        DataGridViewComments.Dock = DockStyle.Fill
        DataGridViewComments.EditMode = DataGridViewEditMode.EditProgrammatically
        DataGridViewComments.Location = New Point(0, 0)
        DataGridViewComments.Name = "DataGridViewComments"
        DataGridViewComments.ReadOnly = True
        DataGridViewComments.RowHeadersVisible = False
        DataGridViewComments.RowTemplate.Height = 25
        DataGridViewComments.Size = New Size(450, 327)
        DataGridViewComments.TabIndex = 4
        ' 
        ' commentSubreddit
        ' 
        commentSubreddit.HeaderText = "Subreddit"
        commentSubreddit.Name = "commentSubreddit"
        commentSubreddit.ReadOnly = True
        ' 
        ' commentSubredditType
        ' 
        commentSubredditType.HeaderText = "Subreddit Type"
        commentSubredditType.Name = "commentSubredditType"
        commentSubredditType.ReadOnly = True
        ' 
        ' commentAuthor
        ' 
        commentAuthor.HeaderText = "Author"
        commentAuthor.Name = "commentAuthor"
        commentAuthor.ReadOnly = True
        ' 
        ' commentAuthorFlairType
        ' 
        commentAuthorFlairType.HeaderText = "Author Flair Type"
        commentAuthorFlairType.Name = "commentAuthorFlairType"
        commentAuthorFlairType.ReadOnly = True
        ' 
        ' commentAuthorIsPremium
        ' 
        commentAuthorIsPremium.HeaderText = "Author Is Premium"
        commentAuthorIsPremium.Name = "commentAuthorIsPremium"
        commentAuthorIsPremium.ReadOnly = True
        ' 
        ' commentTitle
        ' 
        commentTitle.HeaderText = "Title"
        commentTitle.Name = "commentTitle"
        commentTitle.ReadOnly = True
        ' 
        ' commentBody
        ' 
        commentBody.HeaderText = "Body"
        commentBody.Name = "commentBody"
        commentBody.ReadOnly = True
        ' 
        ' commentID
        ' 
        commentID.HeaderText = "ID"
        commentID.Name = "commentID"
        commentID.ReadOnly = True
        ' 
        ' commentPermalink
        ' 
        commentPermalink.HeaderText = "Permalink"
        commentPermalink.Name = "commentPermalink"
        commentPermalink.ReadOnly = True
        ' 
        ' commentUpvotes
        ' 
        commentUpvotes.HeaderText = "Upvotes"
        commentUpvotes.Name = "commentUpvotes"
        commentUpvotes.ReadOnly = True
        ' 
        ' commentDownvotes
        ' 
        commentDownvotes.HeaderText = "Downvotes"
        commentDownvotes.Name = "commentDownvotes"
        commentDownvotes.ReadOnly = True
        ' 
        ' commentScore
        ' 
        commentScore.HeaderText = "Score"
        commentScore.Name = "commentScore"
        commentScore.ReadOnly = True
        ' 
        ' isCommentScoreHidden
        ' 
        isCommentScoreHidden.HeaderText = "Hidden Score"
        isCommentScoreHidden.Name = "isCommentScoreHidden"
        isCommentScoreHidden.ReadOnly = True
        ' 
        ' commentReplies
        ' 
        commentReplies.HeaderText = "Replies"
        commentReplies.Name = "commentReplies"
        commentReplies.ReadOnly = True
        ' 
        ' commentAwards
        ' 
        commentAwards.HeaderText = "Awards"
        commentAwards.Name = "commentAwards"
        commentAwards.ReadOnly = True
        ' 
        ' commentGilded
        ' 
        commentGilded.HeaderText = "Gilded"
        commentGilded.Name = "commentGilded"
        commentGilded.ReadOnly = True
        ' 
        ' commentIsNSFW
        ' 
        commentIsNSFW.HeaderText = "Is NSFW"
        commentIsNSFW.Name = "commentIsNSFW"
        commentIsNSFW.ReadOnly = True
        ' 
        ' commentIsEdited
        ' 
        commentIsEdited.HeaderText = "Is Edited"
        commentIsEdited.Name = "commentIsEdited"
        commentIsEdited.ReadOnly = True
        ' 
        ' commentIsStickied
        ' 
        commentIsStickied.HeaderText = "Is Stickied"
        commentIsStickied.Name = "commentIsStickied"
        commentIsStickied.ReadOnly = True
        ' 
        ' commentIsLocked
        ' 
        commentIsLocked.HeaderText = "Is Locked"
        commentIsLocked.Name = "commentIsLocked"
        commentIsLocked.ReadOnly = True
        ' 
        ' commentIsArchived
        ' 
        commentIsArchived.HeaderText = "Is Archived"
        commentIsArchived.Name = "commentIsArchived"
        commentIsArchived.ReadOnly = True
        ' 
        ' commentIsQuarantined
        ' 
        commentIsQuarantined.HeaderText = "Is Quarantined"
        commentIsQuarantined.Name = "commentIsQuarantined"
        commentIsQuarantined.ReadOnly = True
        ' 
        ' commentCreatedAt
        ' 
        commentCreatedAt.HeaderText = "Posted At"
        commentCreatedAt.Name = "commentCreatedAt"
        commentCreatedAt.ReadOnly = True
        ' 
        ' CommentsWindow
        ' 
        AutoScaleDimensions = New SizeF(7F, 16F)
        AutoScaleMode = AutoScaleMode.Font
        ClientSize = New Size(450, 327)
        Controls.Add(DataGridViewComments)
        Font = New Font("Segoe UI Variable Text", 9F, FontStyle.Regular, GraphicsUnit.Point)
        Icon = CType(resources.GetObject("$this.Icon"), Icon)
        MinimizeBox = False
        Name = "CommentsWindow"
        StartPosition = FormStartPosition.CenterScreen
        Text = "Comments"
        CType(DataGridViewComments, ComponentModel.ISupportInitialize).EndInit()
        ResumeLayout(False)
    End Sub

    Friend WithEvents DataGridViewComments As DataGridView
    Friend WithEvents commentSubreddit As DataGridViewTextBoxColumn
    Friend WithEvents commentSubredditType As DataGridViewTextBoxColumn
    Friend WithEvents commentAuthor As DataGridViewTextBoxColumn
    Friend WithEvents commentAuthorFlairType As DataGridViewTextBoxColumn
    Friend WithEvents commentAuthorIsPremium As DataGridViewTextBoxColumn
    Friend WithEvents commentTitle As DataGridViewTextBoxColumn
    Friend WithEvents commentBody As DataGridViewTextBoxColumn
    Friend WithEvents commentID As DataGridViewTextBoxColumn
    Friend WithEvents commentPermalink As DataGridViewTextBoxColumn
    Friend WithEvents commentUpvotes As DataGridViewTextBoxColumn
    Friend WithEvents commentDownvotes As DataGridViewTextBoxColumn
    Friend WithEvents commentScore As DataGridViewTextBoxColumn
    Friend WithEvents isCommentScoreHidden As DataGridViewTextBoxColumn
    Friend WithEvents commentReplies As DataGridViewTextBoxColumn
    Friend WithEvents commentAwards As DataGridViewTextBoxColumn
    Friend WithEvents commentGilded As DataGridViewTextBoxColumn
    Friend WithEvents commentIsNSFW As DataGridViewTextBoxColumn
    Friend WithEvents commentIsEdited As DataGridViewTextBoxColumn
    Friend WithEvents commentIsStickied As DataGridViewTextBoxColumn
    Friend WithEvents commentIsLocked As DataGridViewTextBoxColumn
    Friend WithEvents commentIsArchived As DataGridViewTextBoxColumn
    Friend WithEvents commentIsQuarantined As DataGridViewTextBoxColumn
    Friend WithEvents commentCreatedAt As DataGridViewTextBoxColumn
End Class
