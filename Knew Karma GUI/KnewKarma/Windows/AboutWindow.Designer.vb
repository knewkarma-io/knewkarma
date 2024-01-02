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
        VersionStatus = New Label()
        ToolTipMainAboutBox = New ToolTip(components)
        ButtonViewLicense = New Button()
        ButtonClose = New Button()
        LabelBuildPlatform = New Label()
        LabelProgramLastName = New Label()
        Copyright = New LinkLabel()
        PictureBox1 = New PictureBox()
        ButtonGetUpdates = New Button()
        Version = New Label()
        Description = New Label()
        CType(PictureBox1, ComponentModel.ISupportInitialize).BeginInit()
        SuspendLayout()
        ' 
        ' LabelProgramFirstName
        ' 
        LabelProgramFirstName.AutoSize = True
        LabelProgramFirstName.Font = New Font("Segoe UI Variable Display", 18F, FontStyle.Bold Or FontStyle.Underline, GraphicsUnit.Point)
        LabelProgramFirstName.ForeColor = SystemColors.ControlText
        LabelProgramFirstName.Location = New Point(203, 19)
        LabelProgramFirstName.Name = "LabelProgramFirstName"
        LabelProgramFirstName.Size = New Size(76, 32)
        LabelProgramFirstName.TabIndex = 3
        LabelProgramFirstName.Text = "Knew"
        ' 
        ' VersionStatus
        ' 
        VersionStatus.AutoSize = True
        VersionStatus.Font = New Font("Segoe UI Variable Display", 9F, FontStyle.Regular, GraphicsUnit.Point)
        VersionStatus.Location = New Point(205, 99)
        VersionStatus.Name = "VersionStatus"
        VersionStatus.Size = New Size(81, 16)
        VersionStatus.TabIndex = 9
        VersionStatus.Text = "Version Status"
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
        ButtonViewLicense.Location = New Point(203, 210)
        ButtonViewLicense.Name = "ButtonViewLicense"
        ButtonViewLicense.Size = New Size(83, 25)
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
        ButtonClose.Location = New Point(396, 210)
        ButtonClose.Name = "ButtonClose"
        ButtonClose.Size = New Size(62, 25)
        ButtonClose.TabIndex = 12
        ButtonClose.Text = "&Close"
        ButtonClose.UseVisualStyleBackColor = False
        ' 
        ' LabelBuildPlatform
        ' 
        LabelBuildPlatform.AutoSize = True
        LabelBuildPlatform.Font = New Font("Segoe UI Variable Display", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        LabelBuildPlatform.Location = New Point(203, 124)
        LabelBuildPlatform.Name = "LabelBuildPlatform"
        LabelBuildPlatform.Size = New Size(74, 15)
        LabelBuildPlatform.TabIndex = 13
        LabelBuildPlatform.Text = "Build platform"
        ' 
        ' LabelProgramLastName
        ' 
        LabelProgramLastName.AutoSize = True
        LabelProgramLastName.BackColor = Color.Transparent
        LabelProgramLastName.Font = New Font("Segoe UI Variable Display", 18F, FontStyle.Underline, GraphicsUnit.Point)
        LabelProgramLastName.ForeColor = Color.FromArgb(CByte(255), CByte(87), CByte(0))
        LabelProgramLastName.Location = New Point(272, 19)
        LabelProgramLastName.Name = "LabelProgramLastName"
        LabelProgramLastName.Size = New Size(81, 32)
        LabelProgramLastName.TabIndex = 14
        LabelProgramLastName.Text = "Karma"
        ' 
        ' Copyright
        ' 
        Copyright.AutoSize = True
        Copyright.Font = New Font("Segoe UI Variable Display", 6.75F, FontStyle.Regular, GraphicsUnit.Point)
        Copyright.Location = New Point(12, 223)
        Copyright.Name = "Copyright"
        Copyright.Size = New Size(44, 12)
        Copyright.TabIndex = 15
        Copyright.TabStop = True
        Copyright.Text = "Copyright"
        ' 
        ' PictureBox1
        ' 
        PictureBox1.BackColor = Color.Transparent
        PictureBox1.Image = CType(resources.GetObject("PictureBox1.Image"), Image)
        PictureBox1.Location = New Point(12, 12)
        PictureBox1.Name = "PictureBox1"
        PictureBox1.Size = New Size(164, 190)
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
        ButtonGetUpdates.Location = New Point(292, 210)
        ButtonGetUpdates.Name = "ButtonGetUpdates"
        ButtonGetUpdates.Size = New Size(98, 25)
        ButtonGetUpdates.TabIndex = 17
        ButtonGetUpdates.Text = "Get Updates"
        ButtonGetUpdates.UseVisualStyleBackColor = True
        ' 
        ' Version
        ' 
        Version.AutoSize = True
        Version.Font = New Font("Segoe UI Variable Display Semil", 18F, FontStyle.Regular, GraphicsUnit.Point)
        Version.Location = New Point(345, 19)
        Version.Name = "Version"
        Version.Size = New Size(88, 32)
        Version.TabIndex = 18
        Version.Text = "Version"
        ' 
        ' Description
        ' 
        Description.AutoSize = True
        Description.Font = New Font("Segoe UI Variable Display Light", 12F, FontStyle.Regular, GraphicsUnit.Point)
        Description.Location = New Point(205, 51)
        Description.Name = "Description"
        Description.Size = New Size(194, 21)
        Description.TabIndex = 19
        Description.Text = "Reddit Data Analysis Toolkit."
        ' 
        ' AboutWindow
        ' 
        AutoScaleDimensions = New SizeF(7F, 16F)
        AutoScaleMode = AutoScaleMode.Font
        BackColor = Color.Gainsboro
        CancelButton = ButtonClose
        ClientSize = New Size(471, 249)
        Controls.Add(Description)
        Controls.Add(Version)
        Controls.Add(ButtonGetUpdates)
        Controls.Add(PictureBox1)
        Controls.Add(Copyright)
        Controls.Add(LabelProgramLastName)
        Controls.Add(LabelBuildPlatform)
        Controls.Add(ButtonClose)
        Controls.Add(ButtonViewLicense)
        Controls.Add(VersionStatus)
        Controls.Add(LabelProgramFirstName)
        DoubleBuffered = True
        Font = New Font("Segoe UI Variable Text", 9F, FontStyle.Regular, GraphicsUnit.Point)
        FormBorderStyle = FormBorderStyle.FixedDialog
        Icon = CType(resources.GetObject("$this.Icon"), Icon)
        MaximizeBox = False
        MinimizeBox = False
        Name = "AboutWindow"
        ShowIcon = False
        ShowInTaskbar = False
        StartPosition = FormStartPosition.CenterScreen
        Text = "About"
        CType(PictureBox1, ComponentModel.ISupportInitialize).EndInit()
        ResumeLayout(False)
        PerformLayout()
    End Sub
    Friend WithEvents LabelProgramFirstName As Label
    Friend WithEvents LicenseRichTextBox As RichTextBox
    Friend WithEvents DataGridView1 As DataGridView
    Friend WithEvents VersionStatus As Label
    Friend WithEvents LabelCopyright As Label
    Friend WithEvents ToolTipMainAboutBox As ToolTip
    Friend WithEvents ButtonViewLicense As Button
    Friend WithEvents ButtonClose As Button
    Friend WithEvents LabelBuildPlatform As Label
    Friend WithEvents LabelProgramLastName As Label
    Friend WithEvents Copyright As LinkLabel
    Friend WithEvents PictureBox1 As PictureBox
    Friend WithEvents ButtonGetUpdates As Button
    Friend WithEvents Version As Label
    Friend WithEvents Description As Label
End Class
