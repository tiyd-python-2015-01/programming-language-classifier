<p><b>diff</b> program output for this 250KB <a href="iofile.php?test=<?=$SelectedTest;?>&amp;file=input">input file</a> (generated with the fasta program N = 25000) with this <a href="iofile.php?test=<?=$SelectedTest;?>&amp;file=output">output file</a> to check your program is correct before contributing.
</p>

<p>We are trying to show the performance of various programming language implementations - so we ask that contributed programs not only give the correct result, but also <b>use the same algorithm</b> to calculate that result.</p>

<p>We use FASTA files generated by the <a href="benchmark.php?test=fasta&amp;lang=all&amp;sort=<?=$Sort;?>">fasta benchmark</a> as input for this benchmark. Note: the file may include both lowercase and uppercase codes.</p>

<p>Each program should</p>
<ul>
  <li>read line-by-line a redirected <a href="http://en.wikipedia.org/wiki/Fasta_format">FASTA format</a> file from stdin</li>
  <li>extract DNA sequence THREE</li>

  <li><b>define a procedure/function</b> to update a hashtable of k-nucleotide keys and count values, for a particular reading-frame &#8212; even though we'll combine k-nucleotide counts for all reading-frames (grow the <b>hashtable</b> from a small default size)</li>
  <li>use that procedure/function and hashtable to
     <ul>
     <li>count <b>all</b> the 1-nucleotide and 2-nucleotide sequences, and write the code and percentage frequency, sorted by descending frequency and then ascending k-nucleotide key</li>
     <li>count <b>all</b> the 3- 4- 6- 12- and 18-nucleotide sequences, and write the count and code for the specific sequences GGT GGTA GGTATT GGTATTTTAATT GGTATTTTAATTTATAGT</li>
      </ul>
   </li>
</ul>


<p>In practice, less brute-force would be used to calculate k-nucleotide frequencies, for example <a href="http://www.biorecipes.com/VirusClassification/code.html">Virus Classification using k-nucleotide Frequencies</a> and <a href="http://www.hicomb.org/HiCOMB2002/papers/HICOMB2003-03.pdf">A Fast Algorithm for the Exhaustive Analysis of 12-Nucleotide-Long DNA Sequences. Applications to Human Genomics</a> (105KB pdf).</p>

