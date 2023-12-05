<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()>
Partial Class SubredditProfileWindow
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
        Dim DataGridViewCellStyle1 As DataGridViewCellStyle = New DataGridViewCellStyle()
        Dim resources As ComponentModel.ComponentResourceManager = New ComponentModel.ComponentResourceManager(GetType(SubredditProfileWindow))
        DataGridViewProfile = New DataGridView()
        DataGridViewHandlerBindingSource = New BindingSource(components)
        CType(DataGridViewProfile, ComponentModel.ISupportInitialize).BeginInit()
        CType(DataGridViewHandlerBindingSource, ComponentModel.ISupportInitialize).BeginInit()
        SuspendLayout()
        ' 
        ' DataGridViewProfile
        ' 
        DataGridViewProfile.AllowUserToAddRows = False
        DataGridViewProfile.AllowUserToDeleteRows = False
        DataGridViewCellStyle1.BackColor = Color.White
        DataGridViewProfile.AlternatingRowsDefaultCellStyle = DataGridViewCellStyle1
        DataGridViewProfile.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill
        DataGridViewProfile.AutoSizeRowsMode = DataGridViewAutoSizeRowsMode.AllCells
        DataGridViewProfile.BackgroundColor = Color.White
        DataGridViewProfile.BorderStyle = BorderStyle.Fixed3D
        DataGridViewProfile.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize
        DataGridViewProfile.ColumnHeadersVisible = False
        DataGridViewProfile.Dock = DockStyle.Fill
        DataGridViewProfile.EditMode = DataGridViewEditMode.EditProgrammatically
        DataGridViewProfile.Location = New Point(0, 0)
        DataGridViewProfile.Name = "DataGridViewProfile"
        DataGridViewProfile.ReadOnly = True
        DataGridViewProfile.RowHeadersVisible = False
        DataGridViewProfile.RowTemplate.Height = 25
        DataGridViewProfile.Size = New Size(570, 384)
        DataGridViewProfile.TabIndex = 0
        ' 
        ' ProfilesWindow
        ' 
        AutoScaleDimensions = New SizeF(7F, 16F)
        AutoScaleMode = AutoScaleMode.Font
        ClientSize = New Size(570, 384)
        Controls.Add(DataGridViewProfile)
        Font = New Font("Segoe UI Variable Display", 9F, FontStyle.Regular, GraphicsUnit.Point)
        FormBorderStyle = FormBorderStyle.FixedDialog
        Icon = CType(resources.GetObject("$this.Icon"), Icon)
        MaximizeBox = False
        MinimizeBox = False
        Name = "ProfilesWindow"
        StartPosition = FormStartPosition.CenterScreen
        Text = "ProfilesWindow"
        CType(DataGridViewProfile, ComponentModel.ISupportInitialize).EndInit()
        CType(DataGridViewHandlerBindingSource, ComponentModel.ISupportInitialize).EndInit()
        ResumeLayout(False)
    End Sub

    Friend WithEvents DataGridViewProfile As DataGridView
    Friend WithEvents DataGridViewHandlerBindingSource As BindingSource
End Class
