Public NotInheritable Class SplashScreen1
    ReadOnly Coreutils As New CoreUtils()

    'TODO: This form can easily be set as the splash screen for the application by going to the "Application" tab
    '  of the Project Designer ("Properties" under the "Project" menu).


    Private Sub SplashScreen1_Load(ByVal sender As Object, ByVal e As System.EventArgs) Handles Me.Load
        Copyright.Text = Coreutils.Copyright
    End Sub

End Class
