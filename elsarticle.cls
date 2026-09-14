%% ---------------------------------------------------------------------------
%% elsarticle.cls -- LOCAL COMPATIBILITY SHIM (article-based)
%% ---------------------------------------------------------------------------
%% The official Elsevier elsarticle.cls was not available in the offline build
%% environment used to produce this manuscript. This shim reproduces the
%% elsarticle *front-matter interface* (frontmatter, \title, \author, \address,
%% \ead, \cortext, \corref, abstract, keyword, highlights, \journal) on top of
%% the standard LaTeX article class so that main.tex compiles unchanged.
%%
%% FOR FINAL ELSEVIER SUBMISSION: install the official class
%%   (TeX Live: `tlmgr install elsarticle`  /  Debian: `texlive-publishers`)
%% and DELETE this local file. main.tex needs no changes; the official class
%% then supplies Elsevier's exact house style and the elsarticle-num.bst.
%% See TODO_before_submission.md.
%% ---------------------------------------------------------------------------
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{elsarticle}[2026/07/17 v0.1 local elsarticle compatibility shim]

\newif\ifels@preprint \els@preprinttrue
\newif\ifels@review   \els@reviewfalse
\def\els@ptsize{12pt}
\DeclareOption{10pt}{\def\els@ptsize{10pt}}
\DeclareOption{11pt}{\def\els@ptsize{11pt}}
\DeclareOption{12pt}{\def\els@ptsize{12pt}}
\DeclareOption{preprint}{\els@preprinttrue}
\DeclareOption{review}{\els@reviewtrue}
\DeclareOption{5p}{}\DeclareOption{3p}{}\DeclareOption{1p}{}
\DeclareOption{twocolumn}{}\DeclareOption{onecolumn}{}
\DeclareOption{times}{}\DeclareOption{final}{}\DeclareOption{authoryear}{}
\DeclareOption{number}{}\DeclareOption{numbers}{}\DeclareOption{sort&compress}{}
\DeclareOption*{}% silently swallow any other elsarticle option
\ProcessOptions\relax
\LoadClass[\els@ptsize]{article}

\RequirePackage[a4paper,margin=1in]{geometry}
\RequirePackage[numbers,sort&compress]{natbib}
% (bibliographystyle is set by main.tex; the shim does not impose one to avoid a
%  duplicate \bibstyle in the .aux)
\RequirePackage{graphicx}
\RequirePackage{textcomp}

\ifels@review\RequirePackage{lineno}\linenumbers\fi
\RequirePackage{setspace}
\ifels@review\onehalfspacing\fi

% ---- journal name ----
\let\els@journal\@empty
\newcommand{\journal}[1]{\gdef\els@journal{#1}}

% ---- author / address accumulation (labels absorbed, names printed inline) ----
\let\els@authors\@empty
\renewcommand{\author}[2][]{%
  \ifx\els@authors\@empty \gdef\els@authors{#2}%
  \else \g@addto@macro\els@authors{\unskip, #2}\fi}
\let\els@addresses\@empty
\newcommand{\address}[2][]{%
  \ifx\els@addresses\@empty \gdef\els@addresses{#2}%
  \else \g@addto@macro\els@addresses{\par #2}\fi}
\newcommand{\affiliation}[2][]{\address[#1]{#2}}
\let\els@ead\@empty
\newcommand{\ead}[2][]{\gdef\els@ead{#2}}
\let\els@cortext\@empty
\newcommand{\cortext}[2][]{\gdef\els@cortext{#2}}
\newcommand{\corref}[1]{\textsuperscript{\(\ast\)}}
\newcommand{\fnref}[1]{}
\newcommand{\tnoteref}[1]{}
\newcommand{\fntext}[2][]{}
\let\els@tnote\@empty
\newcommand{\tnotetext}[2][]{\gdef\els@tnote{#2}}

% ---- abstract / keyword / highlights captured into boxes ----
\newsavebox{\els@absbox}
\renewenvironment{abstract}
  {\begin{lrbox}{\els@absbox}\begin{minipage}{\dimexpr\textwidth-2\fboxsep}%
    \small\noindent{\bfseries Abstract}\par\smallskip\noindent\ignorespaces}
  {\end{minipage}\end{lrbox}\gdef\els@haveabs{1}}
\let\els@haveabs\@empty

\newsavebox{\els@kwbox}
\newcommand{\sep}{;\ }
\newenvironment{keyword}
  {\begin{lrbox}{\els@kwbox}\begin{minipage}{\dimexpr\textwidth-2\fboxsep}%
    \small\noindent{\bfseries Keywords:\ }\ignorespaces}
  {\end{minipage}\end{lrbox}\gdef\els@havekw{1}}
\let\els@havekw\@empty

\newsavebox{\els@hlbox}
\newenvironment{highlights}
  {\begin{lrbox}{\els@hlbox}\begin{minipage}{\dimexpr\textwidth-2\fboxsep}%
    \small\noindent{\bfseries Highlights}\par\smallskip
    \begin{itemize}\setlength{\itemsep}{2pt}\setlength{\parskip}{0pt}}
  {\end{itemize}\end{minipage}\end{lrbox}\gdef\els@havehl{1}}
\let\els@havehl\@empty

% ---- frontmatter environment: end triggers the title block ----
\newenvironment{frontmatter}{}{\els@maketitle}
\newcommand{\els@maketitle}{%
  \thispagestyle{plain}%
  \begin{center}%
    {\LARGE\bfseries\@title\par}%
    \vskip 1.2em
    {\large\els@authors\par}%
    \vskip 0.5em
    {\itshape\small\els@addresses\par}%
    \ifx\els@ead\@empty\else\vskip 0.3em{\small\texttt{\els@ead}\par}\fi
  \end{center}%
  \ifx\els@cortext\@empty\else\vskip 0.2em{\footnotesize\noindent\(\ast\)\,\els@cortext\par}\fi
  \vskip 0.6em\hrule\vskip 0.8em
  \ifx\els@havehl\@empty\else\noindent\usebox{\els@hlbox}\par\vskip 0.8em\fi
  \ifx\els@haveabs\@empty\else\noindent\usebox{\els@absbox}\par\vskip 0.6em\fi
  \ifx\els@havekw\@empty\else\noindent\usebox{\els@kwbox}\par\vskip 0.6em\fi
  \hrule\vskip 1.2em}

\endinput
