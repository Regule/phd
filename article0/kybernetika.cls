%% Class file kybernetika.cls
%% provide style for journal Kybernetika
%% http://www.kybernetika.cz
%%
%% Kybernetika is published by
%% Institute of Information Theory and Automation
%% The Czech Academy of Sciences
%% http://www.utia.cas.cz
%%
%% based on article.cls
%%
%% 2018/10/16 version 1.9.1
%% Pavel Bocek (bocek@utia.cas.cz)
%%
\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{kybernetika}[2018/10/16 v1.9 LaTeX class for Kybernetika Journal]
\newcommand\@ptsize{}
\def\@subdate{????}
\def\@startpage{1}
\def\@doi{}
\def\@hidedoi{}
\def\@hasBW{}
\def\blfootnote{\gdef\@thefnmark{}\@footnotetext}
\newif\if@restonecol
\newif\if@titlepage
\@titlepagefalse
\if@compatibility\else
\DeclareOption{KybPaper}
   {\setlength\paperheight {245mm}%
    \setlength\paperwidth  {172mm}}
\fi
\if@compatibility
  \renewcommand\@ptsize{0}
\else
\DeclareOption{10pt}{\renewcommand\@ptsize{0}}
\fi
\if@compatibility\else
\DeclareOption{twoside}{\@twosidetrue  \@mparswitchtrue}
\fi

\if@compatibility\else
\DeclareOption{final}{\setlength\overfullrule{0pt}}
\fi
\DeclareOption{titlepage}{\@titlepagetrue}
\if@compatibility\else
\DeclareOption{notitlepage}{\@titlepagefalse}
\fi
\if@compatibility\else
\DeclareOption{onecolumn}{\@twocolumnfalse}
\fi
\DeclareOption{openbib}{%
  \AtEndOfPackage{%
   \renewcommand\@openbib@code{%
      \advance\leftmargin\bibindent
      \itemindent -\bibindent
      \listparindent \itemindent
      \parsep \z@
      }%
   \renewcommand\newblock{\par}}%
}
\ExecuteOptions{KybPaper,10pt,twoside,onecolumn,final}
\ProcessOptions
\input{size1\@ptsize.clo}

%% file and procedure for article info dump %% added by PB to article
\newif\if@isBW
\def\setBW{\@isBWtrue}
\def\setdoi#1{\gdef\@doi{#1}}%
\newcommand{\isBW}[2]{\gdef\@hasBW{2}\if@isBW{#1}\else{#2}\fi}
\newcommand{\isCOLOR}[2]{\gdef\@hasBW{3}\if@isBW{#2}\else{#1}\fi}
\newwrite\artdata
\immediate\openout\artdata=kybdata.txt
\def\setstartpage#1{\xdef\@startpage{#1}}%
\def\setdoi#1{\gdef\@doi{#1}}%
\def\hidedoi{\gdef\@hidedoi{1}}%
%%page header set
\newtoks\@kybheader
\def\setheader#1{
\@kybheader{
\null
\vspace*{-16mm}
\footnotesize
\noindent #1
\par\noindent
\rule[3mm]{\textwidth}{0.2mm}
\par
}}%
\newcommand\makeheader{\the\@kybheader}
\newtoks\@kybinfo
\def\@writekybstr#1{\immediate\write\artdata{#1}}
\def\@writekybbeg#1{\@writekybstr{@kybdata_begin:#1}}
\def\@writekybend#1{\@writekybstr{@kybdata_end:#1}}
\def\@writekybinfoexp#1#2{
\@writekybbeg{#1}
\@writekybstr{#2}
\@writekybend{#1}}
\def\@writekybinfo#1#2{
\@kybinfo {#2}%
\@writekybbeg{#1}
\@writekybstr{\the\@kybinfo}
\@writekybend{#1}}
%% end of procedure @writekybinfo
%% finalize article info dump, hook to enddocument
\def\@kybendhook{
\clearpage
\@writekybinfoexp{lastpage}{\thepage}
\@writekybinfoexp{hasBW}{\@hasBW}
\immediate\closeout\artdata}
\let\@enddocumenthook\@kybendhook
\setlength\lineskip{1\p@}
\setlength\normallineskip{1\p@}
\renewcommand\baselinestretch{}
\setlength\parskip{0\p@ \@plus \p@}
\@lowpenalty   51
\@medpenalty  151
\@highpenalty 301
\setcounter{topnumber}{2}
\renewcommand\topfraction{.7}
\setcounter{bottomnumber}{1}
\renewcommand\bottomfraction{.3}
\setcounter{totalnumber}{3}
\renewcommand\textfraction{.2}
\renewcommand\floatpagefraction{.5}
\setcounter{dbltopnumber}{2}
\renewcommand\dbltopfraction{.7}
\renewcommand\dblfloatpagefraction{.5}
%% Kybernetika header font definition % added by PB to article
\newfont{\mi}{cmti9}
\newfont{\mx}{cmr8}
\newfont{\mxs}{cmsl8}
\if@twoside
  \def\ps@headings{%
      \let\@oddfoot\@empty\let\@evenfoot\@empty
      \def\@evenhead{\thepage\hfil\slshape\leftmark}%
      \def\@oddhead{{\slshape\rightmark}\hfil\thepage}%
      \let\@mkboth\markboth
    \def\sectionmark##1{%
      \markboth {\MakeUppercase{%
        \ifnum \c@secnumdepth >\z@
          \thesection\quad
        \fi
        ##1}}{}}%
    \def\subsectionmark##1{%
      \markright {%
        \ifnum \c@secnumdepth >\@ne
          \thesubsection\quad
        \fi
        ##1}}}
\else
  \def\ps@headings{%
    \let\@oddfoot\@empty
    \def\@oddhead{{\slshape\rightmark}\hfil\thepage}%
    \let\@mkboth\markboth
    \def\sectionmark##1{%
      \markright {\MakeUppercase{%
        \ifnum \c@secnumdepth >\m@ne
          \thesection\quad
        \fi
        ##1}}}}
\fi
\def\ps@myheadings{%
    \let\@oddfoot\@empty\let\@evenfoot\@empty
    \def\@evenhead{\thepage\hfil\slshape \MakeUppercase{\mx\leftmark}}%
    \def\@oddhead{{\slshape\mxs\rightmark}\hfil\thepage}%
    \let\@mkboth\@gobbletwo
    \let\sectionmark\@gobble
    \let\subsectionmark\@gobble
    }
\if@titlepage
  \newcommand\maketitle{\begin{titlepage}%
  \let\footnotesize\small
  \let\footnoterule\relax
  \let \footnote \thanks
  \null\vfil
  \vskip 60\p@
  {\large\bf\noindent \MakeUppercase{\@title} \par}%
    \vskip 8mm%
    {\sc \@author \par}%
      \vskip 1.5em%
  \par
  \@thanks
  \vfil\null
  \end{titlepage}%
  \setcounter{footnote}{0}%
  \global\let\thanks\relax
  \global\let\maketitle\relax
  \global\let\@thanks\@empty
  \global\let\@author\@empty
  \global\let\@date\@empty
  \global\let\@title\@empty
  \global\let\title\relax
  \global\let\author\relax
  \global\let\date\relax
  \global\let\and\relax
}
\else
\newcommand\maketitle{\par
  \begingroup
    \renewcommand\thefootnote{\@fnsymbol\c@footnote}%
    \def\@makefnmark{\rlap{\@textsuperscript{\normalfont\@thefnmark}}}%
    \long\def\@makefntext##1{\parindent 1em\noindent
            \hb@xt@1.8em{%
                \hss\@textsuperscript{\normalfont\@thefnmark}}##1}%
   \newpage
   \global\@topnum\z@   % Prevents figures from going at top of page.
   \@maketitle
    \thispagestyle{empty}\@thanks
  \endgroup
  \setcounter{footnote}{0}%
  \global\let\thanks\relax
  \global\let\maketitle\relax
  \global\let\@maketitle\relax
  \global\let\@thanks\@empty
  \global\let\@author\@empty
  \global\let\@date\@empty
  \global\let\@title\@empty
  \global\let\title\relax
  \global\let\author\relax
  \global\let\date\relax
  \global\let\and\relax
}
\def\@maketitle{%% article title and author section %added by PB to article
  \newpage
  \null
  \hypersetup{pdftitle={\@title}}%
  \hypersetup{pdfauthor={\@author}}%
  \hypersetup{pdfcreator={Kybernetika Journal, UTIA}}%
  \the\@kybheader%% article title page header, definition below %added by PB to article
  \vspace*{11mm}
  \let \footnote \thanks
    {\large\bf\noindent
        \fontdimen2\font=1.6\fontdimen2\font
        \MakeUppercase{\@title}
        \fontdimen2\font=0.625\fontdimen2\font
        \par
    }%
     \vskip 8mm%
    {\normalsize \sc \@author \par}%
    \vskip 1em%
  \par
  \if\relax \@hidedoi\relax
    \blfootnote{\hspace{-5mm}DOI: \@doi}
  \fi
  \vskip 20mm}
\fi
\setcounter{secnumdepth}{3}
\newcounter {part}
\newcounter {section}
\newcounter {subsection}[section]
\newcounter {subsubsection}[subsection]
\newcounter {paragraph}[subsubsection]
\newcounter {subparagraph}[paragraph]
\renewcommand\thepart {\@Roman\c@part}
\renewcommand\thesection {\@arabic\c@section}%% dots after counters %added by PB to article
\renewcommand\thesubsection   {\thesection.\@arabic\c@subsection}
\renewcommand\thesubsubsection{\thesubsection.\@arabic\c@subsubsection}
\renewcommand\theparagraph    {\thesubsubsection.\@arabic\c@paragraph}
\renewcommand\thesubparagraph {\theparagraph.\@arabic\c@subparagraph}
\newcommand\part{%
   \if@noskipsec \leavevmode \fi
   \par
   \addvspace{4ex}%
   \@afterindentfalse
   \secdef\@part\@spart}

\def\@part[#1]#2{%
    \ifnum \c@secnumdepth >\m@ne
      \refstepcounter{part}%
      \addcontentsline{toc}{part}{\thepart\hspace{1em}#1}%
    \else
      \addcontentsline{toc}{part}{#1}%
    \fi
    {\parindent \z@ \raggedright
     \interlinepenalty \@M
     \normalfont
     \ifnum \c@secnumdepth >\m@ne
       \Large\bfseries \partname\nobreakspace\thepart
       \par\nobreak
     \fi
     \huge \bfseries #2%
     \markboth{}{}\par}%
    \nobreak
    \vskip 3ex
    \@afterheading}
\def\@spart#1{%
    {\parindent \z@ \raggedright
     \interlinepenalty \@M
     \normalfont
     \huge \bfseries #1\par}%
     \nobreak
     \vskip 3ex
     \@afterheading}
\newcommand\section{\@startsection{section}{1}{3mm}%% absolute indent 3mm %added by PB to article
                                   {-3.25ex \@plus -1ex \@minus -.2ex}%
                                   {1.5ex \@plus .2ex}%
                                   {\uppercase}}
\newcommand\subsection{\@startsection{subsection}{2}{3mm}%
                                     {-3.25ex\@plus -1ex \@minus -.2ex}%
                                     {1.5ex \@plus .2ex}%
                                     {\bf}}
\newcommand\subsubsection{\@startsection{subsubsection}{3}{3mm}%
                                     {-3.25ex\@plus -1ex \@minus -.2ex}%
                                     {1.5ex \@plus .2ex}%
                                     {\normalfont\normalsize}}
\newcommand\paragraph{\@startsection{paragraph}{4}{\z@}%
                                    {3.25ex \@plus1ex \@minus.2ex}%
                                    {-1em}%
                                    {\normalfont\normalsize\bfseries}}
\newcommand\subparagraph{\@startsection{subparagraph}{5}{\parindent}%
                                       {3.25ex \@plus1ex \@minus .2ex}%
                                       {-1em}%
                                      {\normalfont\normalsize\bfseries}}
\setlength\leftmargini  {2.5em}
\leftmargin  \leftmargini
\setlength\leftmarginii  {2.2em}
\setlength\leftmarginiii {1.87em}
\setlength\leftmarginiv  {1.7em}
\setlength\leftmarginv  {1em}
\setlength\leftmarginvi {1em}
\setlength  \labelsep  {.5em}
\setlength  \labelwidth{\leftmargini}
\addtolength\labelwidth{-\labelsep}
\@beginparpenalty -\@lowpenalty
\@endparpenalty   -\@lowpenalty
\@itempenalty     -\@lowpenalty
\renewcommand\theenumi{\@arabic\c@enumi}
\renewcommand\theenumii{\@alph\c@enumii}
\renewcommand\theenumiii{\@roman\c@enumiii}
\renewcommand\theenumiv{\@Alph\c@enumiv}
\newcommand\labelenumi{\theenumi.}
\newcommand\labelenumii{(\theenumii)}
\newcommand\labelenumiii{\theenumiii.}
\newcommand\labelenumiv{\theenumiv.}
\renewcommand\p@enumii{\theenumi}
\renewcommand\p@enumiii{\theenumi(\theenumii)}
\renewcommand\p@enumiv{\p@enumiii\theenumiii}
\newcommand\labelitemi{\textbullet}
\newcommand\labelitemii{\normalfont\bfseries \textendash}
\newcommand\labelitemiii{\textasteriskcentered}
\newcommand\labelitemiv{\textperiodcentered}
%% header of reference section %added by PB to article
\newcommand\refname{R\,E\,F\,E\,R\,E\,N\,C\,E\,S\\
\hspace*{-3mm}
\rule[2mm]{0.993\textwidth}{0.2mm}\\
\vspace*{-6mm}}
%% new commands for keywords, AMS, contact and Proof sections
%% added by PB to article
%% titles of special environments
\newcommand\keywordname{Keywords: }
\newcommand\AMSclassname{Classification: }
\newcommand\Proofname{P\,r\,o\,o\,f\,.\ }
%% keywords
\newcommand\keywords[1]{\noindent{\small{\sl \keywordname}
\begin{minipage}[t]{110mm}#1\end{minipage}}
\vskip 2mm
\@writekybinfo{keywords}{#1}% dump keywords to kybdata.txt
}
%% AMS
\newcommand\classification[1]{\noindent{\small {\sl \AMSclassname}
\begin{minipage}[t]{87mm}#1\end{minipage}}
\vskip 2mm
\@writekybinfo{amses}{#1}% dump ams to kybdata.txt
}
%%submission date set
\def\setsubdate#1{\xdef\@subdate{#1}%
\@writekybinfo{submited}{#1}%
}%
%%submission date print
\newcommand\makesubmdate{
\begin{flushright}
{\footnotesize (Received \@subdate)}
\end{flushright}
}%
%% redef of \title hack to latex.ltx
%% dump title to kybdata.txt
\def\title#1{\def\@title{#1}%
\@writekybinfo{title}{#1}%
}
%% redef of \author hack to latex.ltx
%% dump authors to kybdata.txt
\def\author#1{\def\@author{#1}%
\@writekybinfo{authors}{#1}%
}
%% Proof
\newenvironment{Proof}{%
\medskip\noindent\Proofname\enspace\ignorespaces}{\hfill$\square$}
%% authors contact
%% store list of contacts in contactbuffer
\newtoks\@contactbuffer
\def\contact#1#2#3#4{%
\expandafter\@contactbuffer\expandafter{\the\@contactbuffer \vskip 3mm \par \noindent #1 #2,\, #3\ifx\PBempty#4\PBempty\else\par e-mail: #4\fi}%
%% dump contact info
\@writekybinfo{name}{#1}
\@writekybinfo{surname}{#2}
\@writekybinfo{address}{#3}
\@writekybinfo{email}{#4}
}%

\newcommand\makecontacts{
\normalsize
\par
{\it\the\@contactbuffer}
}

%% some hacks to @startsection and @newtheorem defined in latex.ltx %added by PB to article
%% small skip after sections counter
\def\@seccntformat#1{\csname the#1\endcsname.\enskip}
\def\@xthm#1#2{%
  \@begintheorem{#2}{\csname the#1\endcsname\@thmcountersep}\ignorespaces}
\def\@ythm#1#2[#3]{%
  \@opargbegintheorem{#2}{\csname the#1\endcsname\@thmcountersep}{#3}\ignorespaces}
%% no italic in theorem environment
\def\@begintheorem#1#2{\trivlist
   \item[\hskip \labelsep{\bfseries #1\ #2}]}
\def\@opargbegintheorem#1#2#3{\trivlist
      \item[\hskip \labelsep{\bfseries #1\ #2\ (#3)}]}
%% article title page header called from maketile %added by PB to article
%% if exist file kybhead.tex in current directory use content of file as page header
%% example of kybhead.tex:
%% \setcounter{page}{22}
%% \setsubdate{April 1, 2000}
%% \setheader{\K\,Y\,B\,E\,R\,N\,E\,T\,I\,K\,A\, ---
%% \,V\,O\,L\,U\,M\,E\, {\it 4\,6}\, (\,2\,0\,1\,0\,)\,, \,N\,U\,M\,B\,E\,R\, \,1\,, \,P\,A\,G\,E\,S\, \,2\,2\,--\,2\,4\,}
\newread\testin
\let\next=\relax \openin\testin=kybhead
\ifeof\testin
\setheader{K\,Y\,B\,E\,R\,N\,E\,T\,I\,K\,A\, ---
\,M\,A\,N\,U\,S\,C\,R\,I\,P\,T\, \,P\,R\,E\,V\,I\,E\,W
}
\else \closein\testin
\input kybhead
\fi%
\newenvironment{description}
               {\list{}{\labelwidth\z@ \itemindent-\leftmargin
                        \let\makelabel\descriptionlabel}}
               {\endlist}
\newcommand*\descriptionlabel[1]{\hspace\labelsep
                                \normalfont\bfseries #1}
\if@titlepage
  \newenvironment{abstract}{%
      \titlepage
      \null\vfil
}%
     {\par\vfil\null\endtitlepage}
\else
  \newenvironment{abstract}{%
        \small% no title %added by PB to article
}
      {\par\vspace*{3mm}}%added by PB to article
\fi
\newenvironment{verse}
               {\let\\\@centercr
                \list{}{\itemsep      \z@
                        \itemindent   -1.5em%
                        \listparindent\itemindent
                        \rightmargin  \leftmargin
                        \advance\leftmargin 1.5em}%
                \item\relax}
               {\endlist}
\newenvironment{quotation}
               {\list{}{\listparindent 1.5em%
                        \itemindent    \listparindent
                        \rightmargin   \leftmargin
                        \parsep        \z@ \@plus\p@}%
                \item\relax}
               {\endlist}
\newenvironment{quote}
               {\list{}{\rightmargin\leftmargin}%
                \item\relax}
               {\endlist}
\if@compatibility
\newenvironment{titlepage}
    {%
      \@restonecolfalse\newpage
      \thispagestyle{empty}%
      \setcounter{page}\z@
    }%
    {\newpage
    }
\else
\newenvironment{titlepage}
    {%
        \@restonecolfalse\newpage
      \thispagestyle{empty}%
      \setcounter{page}\@ne
    }%
    {\newpage
    }
\fi
\newcommand\appendix{\par
  \setcounter{section}{0}%
  \setcounter{subsection}{0}%
  \gdef\thesection{\@Alph\c@section}}
\setlength\arraycolsep{5\p@}
\setlength\tabcolsep{6\p@}
\setlength\arrayrulewidth{.4\p@}
\setlength\doublerulesep{2\p@}
\setlength\tabbingsep{\labelsep}
\skip\@mpfootins = \skip\footins
\setlength\fboxsep{3\p@}
\setlength\fboxrule{.4\p@}
\renewcommand \theequation {\@arabic\c@equation}
\newcounter{figure}
\renewcommand \thefigure {\small\@arabic\c@figure}
\def\fps@figure{tbp}
\def\ftype@figure{1}
\def\ext@figure{lof}
\def\fnum@figure{\figurename\nobreakspace\thefigure}
\newenvironment{figure}
               {\@float{figure}}
               {\end@float}
\newenvironment{figure*}
               {\@dblfloat{figure}}
               {\end@dblfloat}
\newcounter{table}
\renewcommand\thetable{\small\@arabic\c@table}
\def\fps@table{tbp}
\def\ftype@table{2}
\def\ext@table{lot}
\def\fnum@table{\tablename\nobreakspace\thetable}
\newenvironment{table}
               {\@float{table}}
               {\end@float}
\newenvironment{table*}
               {\@dblfloat{table}}
               {\end@dblfloat}
\newlength\abovecaptionskip
\newlength\belowcaptionskip
\setlength\abovecaptionskip{10\p@}
\setlength\belowcaptionskip{0\p@}
\long\def\@makecaption#1#2{%
  \vskip\abovecaptionskip
% redef caption env. to minipage max-width 100mm by PB 2011-04-28
\begin{center}
\begin{minipage}[h]{100mm}
\centering
{\bf #1. }{\small #2}
\end{minipage}
\end{center}
  \vskip\belowcaptionskip}
\DeclareOldFontCommand{\rm}{\normalfont\rmfamily}{\mathrm}
\DeclareOldFontCommand{\sf}{\normalfont\sffamily}{\mathsf}
\DeclareOldFontCommand{\tt}{\normalfont\ttfamily}{\mathtt}
\DeclareOldFontCommand{\bf}{\normalfont\bfseries}{\mathbf}
\DeclareOldFontCommand{\it}{\normalfont\itshape}{\mathit}
\DeclareOldFontCommand{\sl}{\normalfont\slshape}{\@nomath\sl}
\DeclareOldFontCommand{\sc}{\normalfont\scshape}{\@nomath\sc}
\DeclareRobustCommand*\cal{\@fontswitch\relax\mathcal}
\DeclareRobustCommand*\mit{\@fontswitch\relax\mathnormal}
\newcommand\@pnumwidth{1.55em}
\newcommand\@tocrmarg{2.55em}
\newcommand\@dotsep{4.5}
\setcounter{tocdepth}{3}
\newcommand\tableofcontents{%
    \section*{\contentsname
        \@mkboth{%
           \MakeUppercase\contentsname}{\MakeUppercase\contentsname}}%
    \@starttoc{toc}%
    }
\newcommand*\l@part[2]{%
  \ifnum \c@tocdepth >-2\relax
    \addpenalty\@secpenalty
    \addvspace{2.25em \@plus\p@}%
    \setlength\@tempdima{3em}%
    \begingroup
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      {\leavevmode
       \large \bfseries #1\hfil \hb@xt@\@pnumwidth{\hss #2}}\par
       \nobreak
       \if@compatibility
         \global\@nobreaktrue
         \everypar{\global\@nobreakfalse\everypar{}}%
      \fi
    \endgroup
  \fi}
\newcommand*\l@section[2]{%
  \ifnum \c@tocdepth >\z@
    \addpenalty\@secpenalty
    \addvspace{1.0em \@plus\p@}%
    \setlength\@tempdima{1.5em}%
    \begingroup
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      \leavevmode \bfseries
      \advance\leftskip\@tempdima
      \hskip -\leftskip
      #1\nobreak\hfil \nobreak\hb@xt@\@pnumwidth{\hss #2}\par
    \endgroup
  \fi}
\newcommand*\l@subsection{\@dottedtocline{2}{1.5em}{2.3em}}
\newcommand*\l@subsubsection{\@dottedtocline{3}{3.8em}{3.2em}}
\newcommand*\l@paragraph{\@dottedtocline{4}{7.0em}{4.1em}}
\newcommand*\l@subparagraph{\@dottedtocline{5}{10em}{5em}}
\newcommand\listoffigures{%
    \section*{\listfigurename}%
      \@mkboth{\MakeUppercase\listfigurename}%
              {\MakeUppercase\listfigurename}%
    \@starttoc{lof}%
    }
\newcommand*\l@figure{\@dottedtocline{1}{1.5em}{2.3em}}
\newcommand\listoftables{%
    \section*{\listtablename}%
      \@mkboth{%
          \MakeUppercase\listtablename}%
         {\MakeUppercase\listtablename}%
    \@starttoc{lot}%
    }
\let\l@table\l@figure
\newdimen\bibindent
\setlength\bibindent{1.5em}
\newenvironment{thebibliography}[1]
     {\small\section*{\refname}%
      \@mkboth{\MakeUppercase\refname}{\MakeUppercase\refname}%
      \list{\@biblabel{\@arabic\c@enumiv}}%
           {\settowidth\labelwidth{\@biblabel{#1}}%
            \leftmargin\labelwidth
            \advance\leftmargin\labelsep
            \@openbib@code
            \usecounter{enumiv}%
            \let\p@enumiv\@empty
            \renewcommand\theenumiv{\@arabic\c@enumiv}}%
      \sloppy
      \clubpenalty4000
      \@clubpenalty \clubpenalty
      \widowpenalty4000%
      \sfcode`\.\@m}
     {\def\@noitemerr
       {\@latex@warning{Empty `thebibliography' environment}}%
      \endlist}
\newcommand\newblock{\hskip .11em\@plus.33em\@minus.07em}
\let\@openbib@code\@empty
\newenvironment{theindex}
               {\twocolumn[\section*{\indexname}]%
                \@mkboth{\MakeUppercase\indexname}%
                        {\MakeUppercase\indexname}%
                \thispagestyle{plain}\parindent\z@
                \parskip\z@ \@plus .3\p@\relax
                \columnseprule \z@
                \columnsep 35\p@
                \let\item\@idxitem}
               {\if@restonecol\onecolumn\else\clearpage\fi}
\newcommand\@idxitem{\par\hangindent 40\p@}
\newcommand\subitem{\@idxitem \hspace*{20\p@}}
\newcommand\subsubitem{\@idxitem \hspace*{30\p@}}
\newcommand\indexspace{\par \vskip 10\p@ \@plus5\p@ \@minus3\p@\relax}
\renewcommand\footnoterule{%
  \kern-3\p@
  \hrule\@width.4\columnwidth
  \kern2.6\p@}
\newcommand\@makefntext[1]{%
    \parindent 1em%
    \noindent
    \hb@xt@1.8em{\hss\@makefnmark}#1}
\newcommand\contentsname{Contents}
\newcommand\listfigurename{List of Figures}
\newcommand\listtablename{List of Tables}
\newcommand\indexname{Index}
\newcommand\figurename{{\small Fig.}}
\newcommand\tablename{{\small Tab.}}
\newcommand\partname{Part}
\newcommand\appendixname{Appendix}
\newcommand\abstractname{Abstract}
\def\today{\ifcase\month\or
  January\or February\or March\or April\or May\or June\or
  July\or August\or September\or October\or November\or December\fi
  \space\number\day, \number\year}
\setlength\columnsep{10\p@}
\setlength\columnseprule{0\p@}
\pagestyle{plain}
\pagenumbering{arabic}
\setcounter{page}{\@startpage}
\if@twoside
\else
  \raggedbottom
\fi
\onecolumn
%% Kybernetika page definition %added by PB to article
\textwidth 134mm
\oddsidemargin -6mm
\evensidemargin -6mm
\textheight 193mm
\topmargin -10mm
\parindent 4.5mm
\baselineskip 5.6mm
\usepackage{graphicx, amssymb, amsmath}
\usepackage{epstopdf}
\usepackage[pdfpagelabels=true, pdfstartview=FitH, pdfpagelayout=TwoPageRight]{hyperref}
\endinput
%%
%% End of file 'kybenetika.cls'.