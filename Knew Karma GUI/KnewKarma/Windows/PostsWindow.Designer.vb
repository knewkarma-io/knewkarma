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
        Dim resources As System.ComponentModel.ComponentResourceManager = New System.ComponentModel.ComponentResourceManager(GetType(PostsWindow))
        DataGridPosts = New DataGridView()
        CType(DataGridPosts, ComponentModel.ISupportInitialize).BeginInit()
        SuspendLayout()
        ' 
        ' DataGridPosts
        ' 
        DataGridPosts.AllowUserToOrderColumns = True
        DataGridPosts.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill
        DataGridPosts.AutoSizeRowsMode = DataGridViewAutoSizeRowsMode.AllCells
        DataGridPosts.BorderStyle = BorderStyle.Fixed3D
        DataGridPosts.CellBorderStyle = DataGridViewCellBorderStyle.Raised
        DataGridPosts.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize
        DataGridPosts.Dock = DockStyle.Fill
        DataGridPosts.Location = New Point(0, 0)
        DataGridPosts.Name = "DataGridPosts"
        DataGridPosts.ReadOnly = True
        DataGridPosts.RowHeadersVisible = False
        DataGridPosts.RowHeadersWidthSizeMode = DataGridViewRowHeadersWidthSizeMode.AutoSizeToAllHeaders
        DataGridPosts.RowTemplate.Height = 25
        DataGridPosts.Size = New Size(450, 327)
        DataGridPosts.TabIndex = 2
        ' 
        ' PostsWindow
        ' 
        AutoScaleDimensions = New SizeF(7F, 16F)
        AutoScaleMode = AutoScaleMode.Font
        ClientSize = New Size(450, 327)
        Controls.Add(DataGridPosts)
        Font = New Font("Segoe UI Variable Text", 9F, FontStyle.Regular, GraphicsUnit.Point)
        Icon = CType(resources.GetObject("$this.Icon"), Icon)
        MinimizeBox = False
        Name = "PostsWindow"
        StartPosition = FormStartPosition.CenterScreen
        Text = "Posts"
        CType(DataGridPosts, ComponentModel.ISupportInitialize).EndInit()
        ResumeLayout(False)
    End Sub

    Friend WithEvents DataGridPosts As DataGridView
End Class
