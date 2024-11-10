<?php

$output = '';
foreach (glob('*.json') as $filename) {
    if ($filename === 'bot_check_results.json') {
        continue;
    }

    $output .= rekap($filename) . PHP_EOL;
}

echo $output;
file_put_contents('rekap.txt', $output);

function rekap($filename)
{
    $output = '';
    $output .= $filename . PHP_EOL;
    $output .= "====================" . PHP_EOL;

    $botsJson = file_get_contents('bot_check_results.json');
    $botsData = json_decode($botsJson, true);

    $json = file_get_contents($filename);
    $data = json_decode($json, true);

    $invalids = [];
    $duplicates = [];
    $bots = [];
    $valid = [];
    $totals = [];
    foreach ($data as $key => $d) {

        $username = $d['username'];
        $comment = $d['text'];
        $timestamp = $d['timestamp'];
        $isBot = $botsData[$username] ?? false;
        $utcDateTime = new DateTime($timestamp, new DateTimeZone('UTC'));
        $utcPlus7DateTime = $utcDateTime->setTimezone(new DateTimeZone('Asia/Jakarta'));
        $date = $utcPlus7DateTime->format('Y-m-d H:i:s');

        if ($date > '2024-11-10 09:00:00') {
            $comment = preg_replace('/[\r\n]/', '', trim($comment));
            $invalids[] = "[$date] $username: $comment";
            continue;
        }

        // $output .= "{$date} {$username}: {$comment} | UTC {$timestamp}" . PHP_EOL;

        preg_match_all('/\d+/', $comment, $matches);
        $vote = strtr((string) implode('', $matches[0]), [
            '0' => '',
            '33' => '3',
        ]);
        $voteNumber = (int) $vote;

        if (isset($valid[$username])) {
            $duplicates[$username] ??= $valid[$username];
            $duplicates[$username] .= "|$voteNumber";
        } else if ($username) {
            if ($voteNumber > 3 || $voteNumber < 1) {
                $comment = preg_replace('/[\r\n]/', '', trim($comment));
                $invalids[] = "[$date] $username: $comment";
            } else {
                $valid[$username] = $voteNumber;

                $totals[$voteNumber] ??= 0;
                $totals[$voteNumber]++;
            }
        }

        // if ($isBot == true) {
        //     $bots[] = $username;
        // }
    }

    if (!empty($invalids)) {
        $output .= "Invalids: " . PHP_EOL;
        foreach ($invalids as $invalid) {
            $output .= "    $invalid" . PHP_EOL;
        }
    }

    if (!empty($bots)) {
        $output .= "Bots: " . PHP_EOL;
        foreach ($bots as $bot) {
            $output .= "    $bot" . PHP_EOL;
        }
    }

    if (!empty($duplicates)) {
        $output .= "Duplicates: " . PHP_EOL;
        foreach ($duplicates as $username => $votes) {
            $output .= "    $username: $votes" . PHP_EOL;
        }
    }

    ksort($totals);

    $output .= "Summary: " . PHP_EOL;
    foreach ($totals as $number => $total) {
        $output .= "    $number: $total" . PHP_EOL;
    }

    $output .= PHP_EOL;

    return $output;
}
