<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class AboutWindow
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
        components = New ComponentModel.Container()
        Dim resources As System.ComponentModel.ComponentResourceManager = New System.ComponentModel.ComponentResourceManager(GetType(AboutWindow))
        LabelProgramFirstName = New Label()
        ToolTipMainAboutBox = New ToolTip(components)
        ButtonViewLicense = New Button()
        ButtonClose = New Button()
        LabelProgramLastName = New Label()
        PictureBox1 = New PictureBox()
        ButtonGetUpdates = New Button()
        Copyright = New Label()
        VersionStatus = New Label()
        CType(PictureBox1, ComponentModel.ISupportInitialize).BeginInit()
        SuspendLayout()
        ' 
        ' LabelProgramFirstName
        ' 
        LabelProgramFirstName.AutoSize = True
        LabelProgramFirstName.Font = New Font("Microsoft Sans Serif", 9F, FontStyle.Bold, GraphicsUnit.Point)
        LabelProgramFirstName.ForeColor = SystemColors.ControlText
        LabelProgramFirstName.Location = New Point(82, 26)
        LabelProgramFirstName.Name = "LabelProgramFirstName"
        LabelProgramFirstName.Size = New Size(42, 15)
        LabelProgramFirstName.TabIndex = 3
        LabelProgramFirstName.Text = "Knew"
        ' 
        ' ToolTipMainAboutBox
        ' 
        ToolTipMainAboutBox.AutoPopDelay = 5000
        ToolTipMainAboutBox.BackColor = Color.Gainsboro
        ToolTipMainAboutBox.InitialDelay = 500
        ToolTipMainAboutBox.ReshowDelay = 100
        ToolTipMainAboutBox.ToolTipIcon = ToolTipIcon.Info
        ToolTipMainAboutBox.ToolTipTitle = "tip"
        ' 
        ' ButtonViewLicense
        ' 
        ButtonViewLicense.FlatStyle = FlatStyle.Popup
        ButtonViewLicense.Font = New Font("Segoe UI Variable Display", 9F, FontStyle.Regular, GraphicsUnit.Point)
        ButtonViewLicense.ForeColor = Color.Black
        ButtonViewLicense.Location = New Point(12, 130)
        ButtonViewLicense.Name = "ButtonViewLicense"
        ButtonViewLicense.Size = New Size(92, 25)
        ButtonViewLicense.TabIndex = 10
        ButtonViewLicense.Text = "View License"
        ButtonViewLicense.UseVisualStyleBackColor = True
        ' 
        ' ButtonClose
        ' 
        ButtonClose.BackColor = Color.Red
        ButtonClose.FlatStyle = FlatStyle.Popup
        ButtonClose.Font = New Font("Segoe UI Variable Display Semib", 9F, FontStyle.Bold, GraphicsUnit.Point)
        ButtonClose.ForeColor = Color.White
        ButtonClose.Location = New Point(252, 130)
        ButtonClose.Name = "ButtonClose"
        ButtonClose.Size = New Size(86, 25)
        ButtonClose.TabIndex = 12
        ButtonClose.Text = "&Close"
        ButtonClose.UseVisualStyleBackColor = False
        ' 
        ' LabelProgramLastName
        ' 
        LabelProgramLastName.AutoSize = True
        LabelProgramLastName.Font = New Font("Microsoft Sans Serif", 9F, FontStyle.Bold, GraphicsUnit.Point)
        LabelProgramLastName.ForeColor = Color.FromArgb(CByte(255), CByte(87), CByte(0))
        LabelProgramLastName.Location = New Point(121, 26)
        LabelProgramLastName.Name = "LabelProgramLastName"
        LabelProgramLastName.Size = New Size(49, 15)
        LabelProgramLastName.TabIndex = 14
        LabelProgramLastName.Text = "Karma"
        ' 
        ' PictureBox1
        ' 
        PictureBox1.Image = CType(resources.GetObject("PictureBox1.Image"), Image)
        PictureBox1.Location = New Point(16, 12)
        PictureBox1.Name = "PictureBox1"
        PictureBox1.Size = New Size(64, 61)
        PictureBox1.SizeMode = PictureBoxSizeMode.Zoom
        PictureBox1.TabIndex = 16
        PictureBox1.TabStop = False
        ' 
        ' ButtonGetUpdates
        ' 
        ButtonGetUpdates.Enabled = False
        ButtonGetUpdates.FlatStyle = FlatStyle.Popup
        ButtonGetUpdates.Font = New Font("Segoe UI Variable Display", 9F, FontStyle.Regular, GraphicsUnit.Point)
        ButtonGetUpdates.ForeColor = Color.Black
        ButtonGetUpdates.Location = New Point(133, 130)
        ButtonGetUpdates.Name = "ButtonGetUpdates"
        ButtonGetUpdates.Size = New Size(89, 25)
        ButtonGetUpdates.TabIndex = 17
        ButtonGetUpdates.Text = "Get Updates"
        ButtonGetUpdates.UseVisualStyleBackColor = True
        ' 
        ' Copyright
        ' 
        Copyright.AutoSize = True
        Copyright.Font = New Font("Segoe UI Variable Display", 8F, FontStyle.Regular, GraphicsUnit.Point)
        Copyright.Location = New Point(80, 52)
        Copyright.Name = "Copyright"
        Copyright.Size = New Size(56, 15)
        Copyright.TabIndex = 20
        Copyright.Text = "Copyright"
        ' 
        ' VersionStatus
        ' 
        VersionStatus.AutoSize = True
        VersionStatus.Font = New Font("Segoe UI Variable Display", 9F, FontStyle.Regular, GraphicsUnit.Point)
        VersionStatus.Location = New Point(272, 25)
        VersionStatus.Name = "VersionStatus"
        VersionStatus.Size = New Size(45, 16)
        VersionStatus.TabIndex = 9
        VersionStatus.Text = "Version"
        ' 
        ' AboutWindow
        ' 
        AutoScaleDimensions = New SizeF(7F, 16F)
        AutoScaleMode = AutoScaleMode.Font
        BackColor = Color.Gainsboro
        CancelButton = ButtonClose
        ClientSize = New Size(350, 168)
        Controls.Add(VersionStatus)
        Controls.Add(Copyright)
        Controls.Add(ButtonGetUpdates)
        Controls.Add(PictureBox1)
        Controls.Add(LabelProgramLastName)
        Controls.Add(ButtonClose)
        Controls.Add(ButtonViewLicense)
        Controls.Add(LabelProgramFirstName)
        DoubleBuffered = True
        Font = New Font("Segoe UI Variable Text", 9F, FontStyle.Regular, GraphicsUnit.Point)
        FormBorderStyle = FormBorderStyle.FixedDialog
        Icon = CType(resources.GetObject("$this.Icon"), Icon)
        MaximizeBox = False
        MinimizeBox = False
        Name = "AboutWindow"
        ShowInTaskbar = False
        StartPosition = FormStartPosition.CenterScreen
        Text = "About Knew Karma"
        CType(PictureBox1, ComponentModel.ISupportInitialize).EndInit()
        ResumeLayout(False)
        PerformLayout()
    End Sub
    Friend WithEvents LabelProgramFirstName As Label
    Friend WithEvents LicenseRichTextBox As RichTextBox
    Friend WithEvents DataGridView1 As DataGridView
    Friend WithEvents LabelCopyright As Label
    Friend WithEvents ToolTipMainAboutBox As ToolTip
    Friend WithEvents ButtonViewLicense As Button
    Friend WithEvents ButtonClose As Button
    Friend WithEvents LabelProgramLastName As Label
    Friend WithEvents PictureBox1 As PictureBox
    Friend WithEvents ButtonGetUpdates As Button
    Friend WithEvents Copyright As Label
    Friend WithEvents VersionStatus As Label
End Class
