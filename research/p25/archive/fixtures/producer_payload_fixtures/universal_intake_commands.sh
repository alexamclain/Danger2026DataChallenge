# P25 KSY/Hilbert-90 universal producer intake fixture commands

PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py --mode hilbert90-signs --eps 1 --branch -1

PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py --mode source-packet --packet research/p25/producer_payload_fixtures/source_packet_target.txt --k-multiplier 1

PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py --mode quotient-factor --base-right-class 1 --base-c 25 --d-right-class 1 --d-c 3 --t-right-class 2 --t-c 113 --k-multiplier 1

PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py --mode source-factor --base-right 25 --base-c 25 --k-right 57 --k-c 0 --d-right 22 --d-c 3 --t-right 38 --t-c 113

PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py --mode compact-theta2 --center-right 44 --center-c 166 --half-right 56 --half-c 28

PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py --mode compact-theta2 --center-right 44 --center-c 166 --half-right 56 --half-c 28 --invert

PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py --mode theta2-sparse --sparse-source research/p25/producer_payload_fixtures/theta2_sparse_target.txt

PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_robert_ksy_theta2_universal_producer_intake.py --mode theta2-sparse --sparse-source research/p25/producer_payload_fixtures/theta2_inverse_sparse_target.txt
