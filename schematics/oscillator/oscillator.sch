EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Device:R R?
U 1 1 60CF3969
P 1650 850
F 0 "R?" V 1443 850 50  0001 C CNN
F 1 "R" V 1535 850 50  0000 C CNN
F 2 "" V 1580 850 50  0001 C CNN
F 3 "~" H 1650 850 50  0001 C CNN
	1    1650 850 
	0    1    1    0   
$EndComp
$Comp
L Device:L L?
U 1 1 60CF474F
P 1350 1150
F 0 "L?" H 1403 1196 50  0001 L CNN
F 1 "L" H 1402 1150 50  0000 L CNN
F 2 "" H 1350 1150 50  0001 C CNN
F 3 "~" H 1350 1150 50  0001 C CNN
	1    1350 1150
	1    0    0    -1  
$EndComp
$Comp
L Device:C C?
U 1 1 60CF521C
P 2000 1150
F 0 "C?" H 2115 1196 50  0001 L CNN
F 1 "C" H 2115 1150 50  0000 L CNN
F 2 "" H 2038 1000 50  0001 C CNN
F 3 "~" H 2000 1150 50  0001 C CNN
	1    2000 1150
	1    0    0    -1  
$EndComp
Wire Wire Line
	1350 1000 1350 850 
Wire Wire Line
	1350 850  1500 850 
Wire Wire Line
	1800 850  2000 850 
Wire Wire Line
	2000 850  2000 1000
Wire Wire Line
	2000 1300 2000 1350
Wire Wire Line
	2000 1350 1350 1350
Wire Wire Line
	1350 1350 1350 1300
$Comp
L Connector:Conn_01x01_Male J?
U 1 1 60CF5D6B
P 1000 850
F 0 "J?" H 1108 1031 50  0001 C CNN
F 1 "Conn_01x01_Male" H 1108 940 50  0001 C CNN
F 2 "" H 1000 850 50  0001 C CNN
F 3 "~" H 1000 850 50  0001 C CNN
	1    1000 850 
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x01_Male J?
U 1 1 60CF6549
P 1000 1350
F 0 "J?" H 1108 1439 50  0001 C CNN
F 1 "Conn_01x01_Male" H 1108 1440 50  0001 C CNN
F 2 "" H 1000 1350 50  0001 C CNN
F 3 "~" H 1000 1350 50  0001 C CNN
	1    1000 1350
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x01_Male J?
U 1 1 60CF6843
P 2400 850
F 0 "J?" H 2372 782 50  0001 R CNN
F 1 "Conn_01x01_Male" H 2372 873 50  0001 R CNN
F 2 "" H 2400 850 50  0001 C CNN
F 3 "~" H 2400 850 50  0001 C CNN
	1    2400 850 
	-1   0    0    1   
$EndComp
$Comp
L Connector:Conn_01x01_Male J?
U 1 1 60CF6E9E
P 2400 1350
F 0 "J?" H 2372 1282 50  0001 R CNN
F 1 "Conn_01x01_Male" H 2372 1373 50  0001 R CNN
F 2 "" H 2400 1350 50  0001 C CNN
F 3 "~" H 2400 1350 50  0001 C CNN
	1    2400 1350
	-1   0    0    1   
$EndComp
Wire Wire Line
	2200 850  2000 850 
Connection ~ 2000 850 
Wire Wire Line
	2200 1350 2000 1350
Connection ~ 2000 1350
Wire Wire Line
	1200 1350 1350 1350
Connection ~ 1350 1350
Wire Wire Line
	1200 850  1350 850 
Connection ~ 1350 850 
$EndSCHEMATC
