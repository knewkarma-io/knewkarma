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

        settings.LoadSettings()
        settings.ToggleSettings(enabled:=settings.DarkMode, saveTo:="darkmode")

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

    Private Sub ButtonCheckforUpdates_Click(sender As Object, e As EventArgs) Handles ButtonGetUpdates.Click
        Shell($"cmd.exe /c start https://github.com/bellingcat/knewkarma/releases/latest")
    End Sub
End Class
