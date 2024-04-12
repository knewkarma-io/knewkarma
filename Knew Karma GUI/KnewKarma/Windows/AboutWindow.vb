Public Class AboutWindow
    ReadOnly settings As New SettingsManager()
    ReadOnly Coreutils As New CoreUtils()

    ''' <summary>
    ''' Handles the Load event for the AboutBox form.
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">The event data.</param>
    Private Async Sub AboutBox_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        ButtonGetUpdates.Enabled = False

        ' Get the system's build version (Operating System version)
        Dim osArchitecture As String = If(Environment.Is64BitOperatingSystem, "64-bit", "32-bit")
        Dim osVersion As String = Environment.OSVersion.Version.ToString()

        Me.Text = $"About {My.Application.Info.AssemblyName}"

        settings.LoadSettings()
        settings.ToggleSettings(enabled:=settings.DarkMode, saveTo:="darkmode")

        LabelBuildPlatform.Text = $"Build platform: {osArchitecture} Windows {osVersion}"
        'Version.Text = $"Version {My.Application.Info.Version}"
        Copyright.Text = Coreutils.Copyright

        Dim ApiHandler As New ApiHandler()
        Await ApiHandler.AsyncGetUpdates()
    End Sub

    ''' <summary>
    ''' Handles the Click event for ButtonViewLicense event. 
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">The event data.</param>
    Private Sub ButtonViewLicense_Click(sender As Object, e As EventArgs) Handles ButtonViewLicense.Click
        CoreUtils.License()
    End Sub

    ''' <summary>
    ''' Handles the Click event for ButtonClose event. 
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">The event data.</param>
    Private Sub ButtonClose_Click(sender As Object, e As EventArgs) Handles ButtonClose.Click
        Me.Close()
    End Sub

    ''' <summary>
    ''' Handles the Click event for Copyright event. 
    ''' </summary>
    ''' <param name="sender">The source of the event.</param>
    ''' <param name="e">The event data.</param>
    Private Sub LinkLabel1_LinkClicked(sender As Object, e As LinkLabelLinkClickedEventArgs) Handles Copyright.LinkClicked, Copyright.LinkClicked
        Shell("cmd.exe /c start https://rly0nheart.github.io")
    End Sub

    Private Sub ButtonCheckforUpdates_Click(sender As Object, e As EventArgs) Handles ButtonGetUpdates.Click
        Shell($"cmd.exe /c start https://github.com/bellingcat/knewkarma/releases/latest")
    End Sub
End Class
