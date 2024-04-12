<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class SplashScreen1
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
        Dim resources As System.ComponentModel.ComponentResourceManager = New System.ComponentModel.ComponentResourceManager(GetType(SplashScreen1))
        Copyright = New Label()
        SuspendLayout()
        ' 
        ' Copyright
        ' 
        Copyright.AutoSize = True
        Copyright.BackColor = Color.Transparent
        Copyright.Font = New Font("Segoe UI Variable Display", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        Copyright.ForeColor = SystemColors.Control
        Copyright.Location = New Point(212, 214)
        Copyright.Name = "Copyright"
        Copyright.Size = New Size(56, 15)
        Copyright.TabIndex = 0
        Copyright.Text = "Copyright"
        ' 
        ' SplashScreen1
        ' 
        AutoScaleDimensions = New SizeF(7F, 15F)
        AutoScaleMode = AutoScaleMode.Font
        BackgroundImage = CType(resources.GetObject("$this.BackgroundImage"), Image)
        BackgroundImageLayout = ImageLayout.Zoom
        ClientSize = New Size(476, 238)
        ControlBox = False
        Controls.Add(Copyright)
        DoubleBuffered = True
        FormBorderStyle = FormBorderStyle.FixedSingle
        MaximizeBox = False
        MinimizeBox = False
        Name = "SplashScreen1"
        ShowInTaskbar = False
        StartPosition = FormStartPosition.CenterScreen
        ResumeLayout(False)
        PerformLayout()

    End Sub

    Friend WithEvents Copyright As Label

End Class