<p><b>diff</b> program output for this 100KB <a href="iofile.php?test=<?=$SelectedTest;?>&amp;file=input">input file</a> (generated with the fasta program N = 10000) with this <a href="iofile.php?test=<?=$SelectedTest;?>&amp;file=output">output file</a> to check your program is correct before contributing.
</p>

<p>We are trying to show the performance of various programming language implementations - so we ask that contributed programs not only give the correct result, but also <b>use the same algorithm</b> to calculate that result.</p>

<p>We use FASTA files generated by the <a href="benchmark.php?test=fasta&amp;lang=all">fasta benchmark</a> as input for this benchmark. Note: the file may include both lowercase and uppercase codes.</p>

<p>Each program should</p>
<ul>
  <li>read all of a redirected <a href="http://en.wikipedia.org/wiki/Fasta_format">FASTA format</a> file from stdin, and record the sequence length</li>
  <li>use the same simple regex pattern match-replace to remove FASTA sequence descriptions and all linefeed characters, and record the sequence length</li>
   <li>use the same simple regex patterns, representing DNA 8-mers and their reverse complement (with a wildcard in one position), and (one pattern at a time) count matches in the redirected file</li>
  <li>write the regex pattern and count</li>
   <li>use the same simple regex patterns to make IUB code alternatives explicit, and (one pattern at a time) match-replace the pattern in the redirect file, and record the sequence length</li>
<li>write the 3 recorded sequence lengths</li>
</ul>

