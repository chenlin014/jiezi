use feature 'say';

my $jm_file1 = $ARGV[0];
my $jm_file2 = $ARGV[1];
my $mb_file =  $ARGV[2];

if(!$mb_file){
	die "Usage: $0 <简码一> <简码二> <码表>";
}

open my $fh, '<', $jm_file1
	or die "无法打开简码一：$_";
my %jm_table1;
while(my $line = <$fh>) {
	chomp($line);
	my ($text, $code) = split /\t/, $line;
	$jm_table1{$text} = $code;
}

open my $fh, '<', $jm_file2
	or die "无法打开简码二：$_";
my %jm_table2;
while(my $line = <$fh>) {
	chomp($line);
	my ($text, $code) = split /\t/, $line;
	$jm_table2{$text} = $code;
}

open my $fh, '<', $mb_file
	or die "无法打开码表：$_";
my %mb;
my %same_code;
my %code2jm1;
my %code2jm2;
while(my $line = <$fh>) {
	chomp($line);
	my ($text, $code) = split /\t/, $line;

	if (!$mb{$code}) {
		$mb{$code} = $text;
	} elsif (!$same_code{$code}) {
		@texts = ($mb{$code}, $text);
		$same_code{$code} = [@texts];
	} else {
		push @{$same_code{$code}}, $text;
	}

	if ($jm_table1{$text}) {
		$code2jm1{$code} = $jm_table1{$text};
	}
	if ($jm_table2{$text}) {
		$code2jm2{$code} = $jm_table2{$text};
	}
}

for my $code (keys %mb) {
	my $jm1 = $code2jm1{$code};
	my $jm2 = $code2jm2{$code};

	if (!($jm1 && $jm2)) {
		next;
	}
	if ($jm1 eq $jm2) {
		next;
	}

	my $text = "";
	if ($same_code{$code}) {
		$text = join(',', @{$same_code{$code}});
	} else {
		$text = $mb{$code}
	}

	say $jm1, ":", $jm2, "\t", $text;
}
