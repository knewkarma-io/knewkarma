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
        Loading = New Label()
        SuspendLayout()
        ' 
        ' Loading
        ' 
        Loading.AutoSize = True
        Loading.BackColor = Color.Transparent
        Loading.Font = New Font("Segoe UI Variable Display", 8.25F, FontStyle.Regular, GraphicsUnit.Point)
        Loading.ForeColor = SystemColors.Control
        Loading.Location = New Point(195, 207)
        Loading.Name = "Loading"
        Loading.Size = New Size(63, 15)
        Loading.TabIndex = 0
        Loading.Text = "Initialising..."
        Loading.UseWaitCursor = True
        ' 
        ' SplashScreen1
        ' 
        AutoScaleDimensions = New SizeF(7F, 15F)
        AutoScaleMode = AutoScaleMode.Font
        BackgroundImage = CType(resources.GetObject("$this.BackgroundImage"), Image)
        BackgroundImageLayout = ImageLayout.Zoom
        ClientSize = New Size(460, 230)
        ControlBox = False
        Controls.Add(Loading)
        DoubleBuffered = True
        FormBorderStyle = FormBorderStyle.FixedSingle
        MaximizeBox = False
        MinimizeBox = False
        Name = "SplashScreen1"
        ShowInTaskbar = False
        StartPosition = FormStartPosition.CenterScreen
        UseWaitCursor = True
        ResumeLayout(False)
        PerformLayout()

    End Sub

    Friend WithEvents Loading As Label

End Class