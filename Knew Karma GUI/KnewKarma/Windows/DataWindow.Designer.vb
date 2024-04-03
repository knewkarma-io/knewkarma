<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()>
Partial Class DataWindow
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
        Dim resources As System.ComponentModel.ComponentResourceManager = New System.ComponentModel.ComponentResourceManager(GetType(DataWindow))
        DataGrid = New DataGridView()
        CType(DataGrid, ComponentModel.ISupportInitialize).BeginInit()
        SuspendLayout()
        ' 
        ' DataGrid
        ' 
        DataGrid.AllowUserToOrderColumns = True
        DataGrid.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill
        DataGrid.AutoSizeRowsMode = DataGridViewAutoSizeRowsMode.AllCells
        DataGrid.CellBorderStyle = DataGridViewCellBorderStyle.Raised
        DataGrid.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize
        DataGrid.ColumnHeadersVisible = False
        DataGrid.Dock = DockStyle.Fill
        DataGrid.EditMode = DataGridViewEditMode.EditProgrammatically
        DataGrid.Location = New Point(0, 0)
        DataGrid.Name = "DataGrid"
        DataGrid.ReadOnly = True
        DataGrid.RowHeadersVisible = False
        DataGrid.RowHeadersWidthSizeMode = DataGridViewRowHeadersWidthSizeMode.AutoSizeToAllHeaders
        DataGrid.RowTemplate.Height = 25
        DataGrid.Size = New Size(450, 327)
        DataGrid.TabIndex = 2
        ' 
        ' DataWindow
        ' 
        AutoScaleDimensions = New SizeF(7F, 16F)
        AutoScaleMode = AutoScaleMode.Font
        ClientSize = New Size(450, 327)
        Controls.Add(DataGrid)
        Font = New Font("Segoe UI Variable Text", 9F, FontStyle.Regular, GraphicsUnit.Point)
        Icon = CType(resources.GetObject("$this.Icon"), Icon)
        Name = "DataWindow"
        StartPosition = FormStartPosition.CenterScreen
        Text = "Data Window"
        CType(DataGrid, ComponentModel.ISupportInitialize).EndInit()
        ResumeLayout(False)
    End Sub

    Friend WithEvents DataGrid As DataGridView
End Class
