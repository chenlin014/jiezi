use utf8;

binmode(STDIN, ":utf8");
binmode(STDOUT, ":utf8");

foreach my $line (<STDIN>) {
	chomp($line);

	my ($text, $code) = split('\t', $line);
	$code =~ s/([^能重])/$1 /g;
	
	if ($code =~ m/^(. . )+[能重]+$/) {
		$code =~ s/(.) (.) 能/$1能 $2/;
		$code =~ s/ 重/重/;
	} else {
		$code =~ s/(.) 能/$1能 /;
	}

	$code =~ s/ $//;

	print "$text\t$code\n";
}
