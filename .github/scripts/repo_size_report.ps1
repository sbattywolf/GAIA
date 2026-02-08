Write-Output "Generating repository size report..."

# Basic repo summary
git count-objects -vH

Write-Output "`nTop 50 largest objects (by size in KB) referenced in history:`n"

# Collect object ids from history
$oids = git rev-list --objects --all 2>$null | ForEach-Object { ($_ -split ' ')[0] } | Sort-Object -Unique

$sizes = @()
foreach ($oid in $oids) {
  try {
    $s = git cat-file -s $oid 2>$null
    if ($s -and ($s -as [int] -gt 0)) {
      $sizes += [PSCustomObject]@{Oid=$oid; Size=[int]$s}
    }
  } catch { }
}

$sizes | Sort-Object -Property Size -Descending | Select-Object -First 50 | ForEach-Object {
  Write-Output ("{0:N0} KB  {1}" -f ($_.Size/1024), $_.Oid)
}

Write-Output "`nList large files currently tracked in working tree (top 50):`n"
git ls-tree -r -l HEAD | ForEach-Object {
  $parts = $_ -split '\s+' 
  # git ls-tree output: mode type oid size	path  (size may be - for submodules)
  if ($parts.Count -ge 4) {
    $size = $parts[$parts.Count-2]
    $path = $parts[-1]
    [PSCustomObject]@{ Size = $size; Path = $path }
  }
} | Where-Object { $_.Size -match '^[0-9]+' } | Sort-Object @{Expression={[int]$_.Size};Descending=$true} | Select-Object -First 50 | ForEach-Object { Write-Output ("{0} bytes    {1}" -f $_.Size, $_.Path) }

Write-Output "`nNote: The history scan can be slow. For a cross-platform report consider running a Python helper or using `git-sizer`/`git rev-list` tooling.`n"
