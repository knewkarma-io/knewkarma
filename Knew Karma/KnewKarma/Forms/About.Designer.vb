<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class About
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
        Dim resources As ComponentModel.ComponentResourceManager = New ComponentModel.ComponentResourceManager(GetType(About))
        LabelProgramFirstName = New Label()
        Version = New Label()
        ToolTipMainAboutBox = New ToolTip(components)
        ButtonViewLicense = New Button()
        ButtonClose = New Button()
        LabelBuildPlatform = New Label()
        LabelProgramLastName = New Label()
        Copyright = New LinkLabel()
        PictureBox1 = New PictureBox()
        ButtonGetUpdates = New Button()
        CType(PictureBox1, ComponentModel.ISupportInitialize).BeginInit()
        SuspendLayout()
        ' 
        ' LabelProgramFirstName
        ' 
        LabelProgramFirstName.AutoSize = True
        LabelProgramFirstName.Font = New Font("Segoe UI Variable Display Semib", 9.75F, FontStyle.Bold, GraphicsUnit.Point)
        LabelProgramFirstName.ForeColor = SystemColors.ControlText
        LabelProgramFirstName.Location = New Point(138, 88)
        LabelProgramFirstName.Name = "LabelProgramFirstName"
        LabelProgramFirstName.Size = New Size(40, 17)
        LabelProgramFirstName.TabIndex = 3
        LabelProgramFirstName.Text = "Knew"
        ' 
        ' Version
        ' 
        Version.AutoSize = True
        Version.Font = New Font("Segoe UI Variable Display", 9F, FontStyle.Regular, GraphicsUnit.Point)
        Version.Location = New Point(119, 109)
        Version.Name = "Version"
        Version.Size = New Size(45, 16)
        Version.TabIndex = 9
        Version.Text = "Version"
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
        ButtonViewLicense.Location = New Point(12, 231)
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
        ButtonClose.Location = New Point(298, 231)
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
        LabelBuildPlatform.Location = New Point(79, 143)
        LabelBuildPlatform.Name = "LabelBuildPlatform"
        LabelBuildPlatform.Size = New Size(74, 15)
        LabelBuildPlatform.TabIndex = 13
        LabelBuildPlatform.Text = "Build platform"
        ' 
        ' LabelProgramLastName
        ' 
        LabelProgramLastName.AutoSize = True
        LabelProgramLastName.Font = New Font("Segoe UI Variable Display Semib", 9.75F, FontStyle.Bold, GraphicsUnit.Point)
        LabelProgramLastName.ForeColor = Color.FromArgb(CByte(255), CByte(87), CByte(0))
        LabelProgramLastName.Location = New Point(174, 88)
        LabelProgramLastName.Name = "LabelProgramLastName"
        LabelProgramLastName.Size = New Size(46, 17)
        LabelProgramLastName.TabIndex = 14
        LabelProgramLastName.Text = "Karma"
        ' 
        ' Copyright
        ' 
        Copyright.AutoSize = True
        Copyright.Font = New Font("Segoe UI Variable Display", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        Copyright.Location = New Point(77, 180)
        Copyright.Name = "Copyright"
        Copyright.Size = New Size(56, 15)
        Copyright.TabIndex = 15
        Copyright.TabStop = True
        Copyright.Text = "Copyright"
        ' 
        ' PictureBox1
        ' 
        PictureBox1.Image = CType(resources.GetObject("PictureBox1.Image"), Image)
        PictureBox1.Location = New Point(138, 12)
        PictureBox1.Name = "PictureBox1"
        PictureBox1.Size = New Size(82, 73)
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
        ButtonGetUpdates.Location = New Point(101, 231)
        ButtonGetUpdates.Name = "ButtonGetUpdates"
        ButtonGetUpdates.Size = New Size(98, 25)
        ButtonGetUpdates.TabIndex = 17
        ButtonGetUpdates.Text = "Get Updates"
        ButtonGetUpdates.UseVisualStyleBackColor = True
        ' 
        ' About
        ' 
        AutoScaleDimensions = New SizeF(7F, 16F)
        AutoScaleMode = AutoScaleMode.Font
        BackColor = Color.Gainsboro
        CancelButton = ButtonClose
        ClientSize = New Size(371, 268)
        Controls.Add(ButtonGetUpdates)
        Controls.Add(PictureBox1)
        Controls.Add(Copyright)
        Controls.Add(LabelProgramLastName)
        Controls.Add(LabelBuildPlatform)
        Controls.Add(ButtonClose)
        Controls.Add(ButtonViewLicense)
        Controls.Add(Version)
        Controls.Add(LabelProgramFirstName)
        DoubleBuffered = True
        Font = New Font("Segoe UI Variable Text", 9F, FontStyle.Regular, GraphicsUnit.Point)
        FormBorderStyle = FormBorderStyle.FixedDialog
        Icon = CType(resources.GetObject("$this.Icon"), Icon)
        MaximizeBox = False
        MinimizeBox = False
        Name = "About"
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
    Friend WithEvents Version As Label
    Friend WithEvents LabelCopyright As Label
    Friend WithEvents ToolTipMainAboutBox As ToolTip
    Friend WithEvents ButtonViewLicense As Button
    Friend WithEvents ButtonClose As Button
    Friend WithEvents LabelBuildPlatform As Label
    Friend WithEvents LabelProgramLastName As Label
    Friend WithEvents Copyright As LinkLabel
    Friend WithEvents PictureBox1 As PictureBox
    Friend WithEvents ButtonGetUpdates As Button
End Class
