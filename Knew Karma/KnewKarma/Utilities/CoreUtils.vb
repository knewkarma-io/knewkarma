Imports System.IO
Imports Microsoft.Win32
Imports Newtonsoft.Json
Imports Newtonsoft.Json.Linq
Imports System.Globalization

Public Class CoreUtils
    ''' <summary>
    ''' Handles the enabling and disabling of various controls based on the state of radio buttons on the main form.
    ''' </summary>
    ''' <param name="form">The main form containing the radio buttons and controls to be manipulated.</param>
    Public Shared Sub HandleRadioButtonChanges(form As Main)
        ' Check the state of user radio buttons and enable/disable relevant controls accordingly
        ' Depending on which radio button is selected, different sets of controls will be enabled or disabled
        ' to provide a more intuitive user experience and prevent invalid configurations.

        ' Handling User Radio Buttons
        If form.RadioButtonUserProfile.Checked Then
            ' If the User Profile radio button is checked, disable the user data limit and posts listing controls
            form.NumericUpDownUserDataLimit.Enabled = False
            form.ComboBoxUserPostsListing.Enabled = False
        ElseIf form.RadioButtonUserPosts.Checked Then
            ' If the User Posts radio button is checked, enable the user data limit and posts listing controls
            form.NumericUpDownUserDataLimit.Enabled = True
            form.ComboBoxUserPostsListing.Enabled = True
        ElseIf form.RadioButtonUserComments.Checked Then
            ' If the User Comments radio button is checked, enable the user data limit control and disable the posts listing control
            form.NumericUpDownUserDataLimit.Enabled = True
            form.ComboBoxUserPostsListing.Enabled = True
        End If

        ' Handling Subreddit Radio Buttons
        ' Similar to the user radio buttons above, check the state of subreddit radio buttons
        ' and enable/disable the corresponding controls to ensure a coherent set of options is available to the user.

        If form.RadioButtonSubredditProfile.Checked Then
            ' If the Subreddit Profile radio button is checked, disable the subreddit data limit and posts listing controls
            form.NumericUpDownSubredditDataLimit.Enabled = False
            form.ComboBoxSubredditPostsListing.Enabled = False
        ElseIf form.RadioButtonSubredditPosts.Checked Then
            ' If the Subreddit Posts radio button is checked, enable the subreddit data limit and posts listing controls
            form.NumericUpDownSubredditDataLimit.Enabled = True
            form.ComboBoxSubredditPostsListing.Enabled = True
        End If

        If form.RadioButtonPostProfile.Checked Then
            form.NumericUpDownPostDataLimit.Enabled = False
            form.ComboBoxPostDataListing.Enabled = False
        ElseIf form.RadioButtonPostComments.Checked Then
            form.NumericUpDownPostDataLimit.Enabled = True
            form.ComboBoxPostDataListing.Enabled = True
        End If
    End Sub

    ''' <summary>
    ''' Determines if the Windows system theme is in dark mode.
    ''' </summary>
    ''' <returns>
    ''' True if the dark mode is enabled, otherwise false.
    ''' </returns>
    Public Shared Function IsSystemDarkTheme() As Boolean
        Dim registryKey As RegistryKey = Registry.CurrentUser.OpenSubKey("Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        If registryKey IsNot Nothing Then
            Dim appsUseLightTheme As Object = registryKey.GetValue("AppsUseLightTheme")
            Return appsUseLightTheme IsNot Nothing AndAlso CType(appsUseLightTheme, Integer) = 0
        Else
            Return False
        End If
    End Function

    ''' <summary>
    ''' Asynchronously checks for available updates and optionally displays a message to the user.
    ''' </summary>
    ''' <param name="IsAutoCheck">Indicates whether the update check is triggered automatically.</param>
    ''' <returns>A task representing the asynchronous operation.</returns>
    Public Shared Async Function AsyncCheckUpdates() As Task
        About.Version.Text = "Checking for Updates..."
        ' Creating a new instance of the ApiHandler class to interact with the API.
        Dim Api As New ApiHandler()

        ' Making an asynchronous request to check for updates.
        Dim data As JObject = Await Api.AsyncGetUpdates()

        ' Checking if data is not null before proceeding with extracting information from it.
        If data IsNot Nothing Then
            ' Extracting the tag name, body, and HTML URL from the data.
            Dim tagName As String = data("tag_name")?.ToString

            ' Checking if the current version is the latest version.
            If tagName = My.Application.Info.Version.ToString Then
                About.Version.Text = $"Up-to-date ({My.Application.Info.Version})"
            Else
                About.Version.Text = $"Updates found ({tagName})"
                About.ButtonGetUpdates.Enabled = True
            End If
        End If
    End Function

    ''' <summary>
    ''' Checks whether the given JSON data (either JObject or JArray) is null or empty.
    ''' </summary>
    ''' <param name="data">The JToken (JObject/JArray) to be validated.</param>
    ''' <returns>True if the data is not null and contains an "id" key, otherwise False.</returns>
    Public Shared Function IsValidData(data As JToken) As Boolean
        If data IsNot Nothing AndAlso (
        (TypeOf data Is JArray AndAlso DirectCast(data, JArray).Any()) OrElse
        (TypeOf data Is JObject AndAlso (data("id") IsNot Nothing))
    ) Then
            Return True
        Else
            Return False
        End If
    End Function

    ''' <summary>
    ''' Converts a Unix timestamp with possible decimal points to a formatted datetime string.
    ''' </summary>
    ''' <param name="timestamp">The Unix timestamp to be converted.</param>
    ''' <returns>A formatted datetime string in the format "dd MMMM yyyy, hh:mm:ss.fff tt".</returns>
    Public Shared Function ConvertTimestampToDatetime(ByVal timestamp As Double) As String
        Dim utcFromTimestamp As Date = New DateTime(1970, 1, 1, 0, 0, 0, DateTimeKind.Utc).AddSeconds(timestamp)
        Dim datetimeString As String = utcFromTimestamp.ToString("dd MMMM yyyy, hh:mm:ss tt", CultureInfo.InvariantCulture)
        Return datetimeString
    End Function

    ''' <summary>
    ''' Shows the license notice in a messagebox.
    ''' </summary>
    Public Shared Sub License()
        MessageBox.Show($"{My.Application.Info.Copyright}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the ""Software""), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED ""AS IS"", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.", "MIT License", MessageBoxButtons.OK, MessageBoxIcon.Information)
    End Sub

    ''' <summary>
    ''' Checks for the existence of the 'Knew Karma' directory within the user's AppData\Roaming folder. 
    ''' If the directory does not exist, it creates one.
    ''' </summary>
    Public Shared Sub PathFinder()
        Dim directoryPath As String = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "Knew Karma")

        If Not Directory.Exists(directoryPath) Then
            Directory.CreateDirectory(directoryPath)
        End If
    End Sub

    ''' <summary>
    ''' Prompts the user to save the data in either JSON or CSV format based on the settings specified in FormMain.
    ''' </summary>
    ''' <param name="data">The data to save, represented as a JToken, which can accommodate both JArray and JObject.</param>
    Public Shared Sub PromptSaveData(data As JToken, title As String)
        ' Save profile data to JSON if the JSON toolStripMenuItem is checked.
        If Main.settings.SaveToJson Then
            SaveDataToJson(data:=data, title:=title)
        End If
        ' Save profile data to CSV if the CSV toolStripMenuItem is checked.
        If Main.settings.SaveToCsv Then
            SaveDataToCSV(data:=data, title:=title)
        End If
    End Sub

    ''' <summary>
    ''' Saves the provided data to a JSON file.
    ''' </summary>
    ''' <param name="data">The data to save, which can be a JObject or a JArray.</param>
    ''' <param name="title">The title to use in the SaveFileDialog and the success message.</param>
    Private Shared Sub SaveDataToJson(data As JToken, title As String)
        ' Initialize a new SaveFileDialog with the specified filter and title
        Dim saveFileDialog As New SaveFileDialog With {
            .Filter = "JSON files (*.json)|*.json",
            .title = $"Save data to JSON"
        }

        ' Open the SaveFileDialog and if the result is OK, proceed to save the data
        If saveFileDialog.ShowDialog() = DialogResult.OK Then
            Dim fileName As String = saveFileDialog.FileName

            ' Check if the data is not null and has values before proceeding to serialize it
            If data Is Nothing OrElse (TypeOf data Is JArray AndAlso Not CType(data, JArray).HasValues) OrElse (TypeOf data Is JObject AndAlso Not CType(data, JObject).HasValues) Then
                MessageBox.Show("Empty or null data cannot be saved.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error)
                Exit Sub
            End If

            ' Define serializer settings to format the JSON string nicely
            Dim serializerSettings As New JsonSerializerSettings With {
                .Formatting = Formatting.Indented
            }

            ' Serialize the JToken (which could be a JArray or a JObject) to a JSON string with the defined settings
            Dim json As String = JsonConvert.SerializeObject(data, serializerSettings)

            ' Write the JSON string to a file with the specified file name
            File.WriteAllText(fileName, json)

            ' Show a message indicating that the data has been successfully saved
            MessageBox.Show($"{title} data saved to {fileName}", "Saved", MessageBoxButtons.OK, MessageBoxIcon.Information)
        End If
    End Sub

    ''' <summary>
    ''' Saves the provided data to a CSV file.
    ''' </summary>
    ''' <param name="data">The data to save, which can be a JObject or a JArray.</param>
    ''' <param name="title">The title to use in the SaveFileDialog and the success message.</param>
    Private Shared Sub SaveDataToCSV(data As JToken, title As String)
        ' Initialize a new SaveFileDialog with the specified filter and title
        Dim saveFileDialog As New SaveFileDialog With {
            .Filter = "CSV files (*.csv)|*.csv",
            .title = $"Save data to CSV"
        }

        ' Open the SaveFileDialog and if the result is OK, proceed to save the data
        If saveFileDialog.ShowDialog() = DialogResult.OK Then
            Dim fileName As String = saveFileDialog.FileName

            ' Create a new StreamWriter to write data to the CSV file
            Using csvWriter As New StreamWriter(fileName)
                ' Variable to store the headers obtained from the data
                Dim headers As String() = Nothing

                ' Check if the data is a JArray and has values, and if true, get the headers from the first JObject in the JArray
                If TypeOf data Is JArray AndAlso data.HasValues Then
                    headers = CType(data(0), JObject).Properties().Select(Function(p) p.Name).ToArray()
                    ' Check if the data is a JObject and has values, and if true, get the headers from the JObject
                ElseIf TypeOf data Is JObject AndAlso data.HasValues Then
                    headers = CType(data, JObject).Properties().Select(Function(p) p.Name).ToArray()
                End If

                ' If headers are not obtained, show an error message and exit the subroutine
                If headers Is Nothing OrElse Not headers.Any() Then
                    MessageBox.Show("Unsupported data type or empty data.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error)
                    Exit Sub
                End If

                ' Write the headers to the CSV file
                csvWriter.WriteLine(String.Join(",", headers))

                ' Create an IEnumerable of JObject to handle both JArray and JObject cases
                ' If it's a JArray, cast it to IEnumerable of JObject
                ' If it's a JObject, create a new array with this single JObject
                Dim dataRows As IEnumerable(Of JObject) = If(TypeOf data Is JArray, CType(data, JArray).Cast(Of JObject)(), New JObject() {CType(data, JObject)})

                ' Loop through each row in dataRows to write the data to the CSV file
                For Each row In dataRows
                    ' For each header, get the corresponding value from the current row (if it exists, otherwise use "N/A")
                    ' and write this set of values to the CSV file
                    Dim values = headers.Select(Function(header) If(row(header)?.ToString(), "N/A")).ToArray()
                    csvWriter.WriteLine(String.Join(",", values))
                Next
            End Using

            ' Show a message to indicate that the data has been successfully saved
            MessageBox.Show($"{title} saved to {fileName}", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information)
        End If
    End Sub
End Class
