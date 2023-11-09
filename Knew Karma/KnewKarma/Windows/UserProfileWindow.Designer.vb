<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class UserProfileWindow
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
        Dim DataGridViewCellStyle2 As DataGridViewCellStyle = New DataGridViewCellStyle()
        Dim resources As ComponentModel.ComponentResourceManager = New ComponentModel.ComponentResourceManager(GetType(UserProfileWindow))
        TabControl1 = New TabControl()
        TabPage1 = New TabPage()
        DataGridViewUserProfile = New DataGridView()
        TabPage2 = New TabPage()
        DataGridViewUserSubreddit = New DataGridView()
        TabControl1.SuspendLayout()
        TabPage1.SuspendLayout()
        CType(DataGridViewUserProfile, ComponentModel.ISupportInitialize).BeginInit()
        TabPage2.SuspendLayout()
        CType(DataGridViewUserSubreddit, ComponentModel.ISupportInitialize).BeginInit()
        SuspendLayout()
        ' 
        ' TabControl1
        ' 
        TabControl1.Controls.Add(TabPage1)
        TabControl1.Controls.Add(TabPage2)
        TabControl1.Dock = DockStyle.Fill
        TabControl1.Location = New Point(0, 0)
        TabControl1.Name = "TabControl1"
        TabControl1.SelectedIndex = 0
        TabControl1.Size = New Size(410, 250)
        TabControl1.TabIndex = 0
        ' 
        ' TabPage1
        ' 
        TabPage1.Controls.Add(DataGridViewUserProfile)
        TabPage1.Location = New Point(4, 24)
        TabPage1.Name = "TabPage1"
        TabPage1.Padding = New Padding(3)
        TabPage1.Size = New Size(402, 222)
        TabPage1.TabIndex = 0
        TabPage1.Text = "Profile"
        TabPage1.UseVisualStyleBackColor = True
        ' 
        ' DataGridViewUserProfile
        ' 
        DataGridViewUserProfile.AllowUserToAddRows = False
        DataGridViewUserProfile.AllowUserToDeleteRows = False
        DataGridViewCellStyle1.BackColor = Color.White
        DataGridViewUserProfile.AlternatingRowsDefaultCellStyle = DataGridViewCellStyle1
        DataGridViewUserProfile.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill
        DataGridViewUserProfile.AutoSizeRowsMode = DataGridViewAutoSizeRowsMode.AllCells
        DataGridViewUserProfile.BackgroundColor = Color.White
        DataGridViewUserProfile.BorderStyle = BorderStyle.None
        DataGridViewUserProfile.CellBorderStyle = DataGridViewCellBorderStyle.Raised
        DataGridViewUserProfile.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize
        DataGridViewUserProfile.ColumnHeadersVisible = False
        DataGridViewUserProfile.Dock = DockStyle.Fill
        DataGridViewUserProfile.EditMode = DataGridViewEditMode.EditProgrammatically
        DataGridViewUserProfile.Location = New Point(3, 3)
        DataGridViewUserProfile.Name = "DataGridViewUserProfile"
        DataGridViewUserProfile.ReadOnly = True
        DataGridViewUserProfile.RowHeadersVisible = False
        DataGridViewUserProfile.RowTemplate.Height = 25
        DataGridViewUserProfile.Size = New Size(396, 216)
        DataGridViewUserProfile.TabIndex = 1
        ' 
        ' TabPage2
        ' 
        TabPage2.Controls.Add(DataGridViewUserSubreddit)
        TabPage2.Location = New Point(4, 24)
        TabPage2.Name = "TabPage2"
        TabPage2.Padding = New Padding(3)
        TabPage2.Size = New Size(402, 222)
        TabPage2.TabIndex = 1
        TabPage2.Text = "Subreddit"
        TabPage2.UseVisualStyleBackColor = True
        ' 
        ' DataGridViewUserSubreddit
        ' 
        DataGridViewUserSubreddit.AllowUserToAddRows = False
        DataGridViewUserSubreddit.AllowUserToDeleteRows = False
        DataGridViewCellStyle2.BackColor = Color.White
        DataGridViewUserSubreddit.AlternatingRowsDefaultCellStyle = DataGridViewCellStyle2
        DataGridViewUserSubreddit.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill
        DataGridViewUserSubreddit.AutoSizeRowsMode = DataGridViewAutoSizeRowsMode.AllCells
        DataGridViewUserSubreddit.BackgroundColor = Color.White
        DataGridViewUserSubreddit.BorderStyle = BorderStyle.None
        DataGridViewUserSubreddit.CellBorderStyle = DataGridViewCellBorderStyle.Raised
        DataGridViewUserSubreddit.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize
        DataGridViewUserSubreddit.ColumnHeadersVisible = False
        DataGridViewUserSubreddit.Dock = DockStyle.Fill
        DataGridViewUserSubreddit.EditMode = DataGridViewEditMode.EditProgrammatically
        DataGridViewUserSubreddit.Location = New Point(3, 3)
        DataGridViewUserSubreddit.Name = "DataGridViewUserSubreddit"
        DataGridViewUserSubreddit.ReadOnly = True
        DataGridViewUserSubreddit.RowHeadersVisible = False
        DataGridViewUserSubreddit.RowTemplate.Height = 25
        DataGridViewUserSubreddit.Size = New Size(396, 216)
        DataGridViewUserSubreddit.TabIndex = 1
        ' 
        ' UserProfileWindow
        ' 
        AutoScaleDimensions = New SizeF(7F, 15F)
        AutoScaleMode = AutoScaleMode.Font
        ClientSize = New Size(410, 250)
        Controls.Add(TabControl1)
        FormBorderStyle = FormBorderStyle.FixedSingle
        Icon = CType(resources.GetObject("$this.Icon"), Icon)
        MaximizeBox = False
        MinimizeBox = False
        Name = "UserProfileWindow"
        StartPosition = FormStartPosition.CenterScreen
        Text = "UserProfileWindow"
        TabControl1.ResumeLayout(False)
        TabPage1.ResumeLayout(False)
        CType(DataGridViewUserProfile, ComponentModel.ISupportInitialize).EndInit()
        TabPage2.ResumeLayout(False)
        CType(DataGridViewUserSubreddit, ComponentModel.ISupportInitialize).EndInit()
        ResumeLayout(False)
    End Sub

    Friend WithEvents TabControl1 As TabControl
    Friend WithEvents TabPage1 As TabPage
    Friend WithEvents TabPage2 As TabPage
    Friend WithEvents DataGridViewUserProfile As DataGridView
    Friend WithEvents DataGridViewUserSubreddit As DataGridView
End Class
