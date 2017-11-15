# RPM research tools
## Introduction
	This package contains some tools for investigate constituion of OpenHPC.

	1. lsrpm.py display rpm package information in the specified directory.
	2. compare-pkgs.py show the difference rpms in the two directories.

## Preparation
Type the following command as root privilege:

sudo yum install -y  python-pandas numpy

## How to run commands
### lsrpm.py

Specify the directory which contains binary rpm packages.
This command search rpm packages in the directory recusively if subdirectories exist.
This print the target architecture, the package name, the group, version, summary, license, and size
in CSV format to standard output.

	>
	> lsrpm.py Directory
	>
	
	example
	> ./lsrpm.py ./OpenHPCv1.3 > OpenHPCv1.3.txt

### compare-pkgs.py
This command comapre rpm files in two directories, 

Once this command removes the suffixes(-ohpc, -orch) in package names and then the command compare
each packages using converted package name as key.

This command shows target architecture, package name, version of packages in the first directory,
version of packages in the second directory, comparison versions between packages, package summary
to standard output(CSV format).


Synopsis
>	
> compare-pkgs.py -f first-directory -s second-directory
>	
	
Example
>
> ./compare-pkgs.py -f ./OpenHPCv1.2 -s ./OpenHPCv1.3
>

## Typical usage

For example, if you want to compare OpenHPCv1.2 and OpenHPCv1.3,
download all packages for each version into each different directories.

1. Store PRM packages in OpenHPC v1.2 into v1_2 directory:
   > mkdir v1_2
   > cd v1_2
   > wget -r -l1 -A .rpm -nd http://build.openhpc.community/OpenHPC:/1.2/CentOS_7.2/x86_64
   > wget -r -l1 -A .rpm -nd http://build.openhpc.community/OpenHPC:/1.2/CentOS_7.2/noarch
   > cd ..
2. Store PRM packages in OpenHPC v1.3 into v1_3 directory:
   > mkdir v1_3
   > cd v1_3
   > wget -r -l1 -A .rpm -nd http://build.openhpc.community/OpenHPC:/1.3/CentOS_7/x86_64
   > wget -r -l1 -A .rpm -nd http://build.openhpc.community/OpenHPC:/1.3/CentOS_7/noarch
   > cd ..
3. Print package constitution in OpenHPC v1.2 using lsrpm.py:
   > ./lsrpm.py v1_2 > OpenHPCv1_2.txt
4. Print package constitution in OpenHPC v1.3 using lsrpm.py:
   > ./lsrpm.py v1_3 > OpenHPCv1_3.txt
5. Compare OpenHPC v1.2 and OpenHPC v1.3 using compare-pkgs.py:
   > ./compare-pkgs.py -f ./v1_2 -s ./v1_3
   
   
