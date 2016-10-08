On Error Resume Next

Set wshShell = WScript.CreateObject("WScript.Shell")
wshShell.CurrentDirectory = "flask"
cmd = "python flaskr.py"
wshShell.Run cmd

Dim oXMLHTTP, maxTries, url
url = "http://127.0.0.1:5000"
Set oXMLHTTP = CreateObject("MSXML2.XMLHTTP.3.0")
oXMLHTTP.Open "GET", url, False
oXMLHTTP.Send

For maxTries = 1 To 10

  If err.number <> 0 then 
    line =""
    Line  = Line &  vbcrlf & "" 
    Line  = Line &  vbcrlf & "Error getting file" 
    Line  = Line &  vbcrlf & "==================" 
    Line  = Line &  vbcrlf & "" 
    Line  = Line &  vbcrlf & "Error " & err.number & "(0x" & hex(err.number) & ") " & err.description 
    Line  = Line &  vbcrlf & "Source " & err.source 
    Line  = Line &  vbcrlf & "" 
    Line  = Line &  vbcrlf & "HTTP Error " & File.Status & " " & File.StatusText
    Line  = Line &  vbcrlf &  File.getAllResponseHeaders
'   wscript.echo Line
    Err.clear
'    wscript.quit

    If oXMLHTTP.Status <> 200 and maxTries > 0 Then
 	oXMLHTTP.Open "GET", url, False
  	oXMLHTTP.Send
	WScript.Sleep 2000
    End If
  Else   
    Exit For
  End If
Next

wshShell.Run "chrome "& url
