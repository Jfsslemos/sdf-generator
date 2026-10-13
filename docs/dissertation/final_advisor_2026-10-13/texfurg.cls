%==============================================================================
% Identificação
%==============================================================================
\def\currversion{19/11/2020}

\typeout{^^J^^J
--------------------------------------------------^^J
CLASSE texfurg^^J
Formatação de Documentos do Centro de Ciências Computacionais da FURG^^J
--------------------------------------------------^^J
Desenvolvida a partir da Classe IIUFRGS^^J
por Marilton S. de Aguiar (marilton@inf.ufpel.edu.br)^^J
Atualização^^J
Eder Mateus Nunes Gon\c{c}alves - C3-FURG (edergoncalves@furg.br)^^J
Novembro 2020^^J
--------------------------------------------------^^J
Versão: \currversion^^J
--------------------------------------------------^^J^^J}

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{texfurg}[\currversion]

%==============================================================================
% Declaração de opções
%==============================================================================
\newcommand{\eiu@novodoc}[1]{\DeclareOption{#1}{\AtEndOfClass{\input{#1.def}}}}
\eiu@novodoc{tcc}
\eiu@novodoc{ti} 
\eiu@novodoc{qua}
\eiu@novodoc{dm} 

\newcommand{\bibliotecario}[1]{\gdef\@nomebibliotecario{#1}}
\newcommand{\biblioteca}[1]{\gdef\@nomebiblioteca{#1}}
\newcommand{\cipdata}[2]{\gdef\@codigocip{#1}\gdef\@codigocdd{#2}}

\newcommand{\course}[1]{\gdef\@course{#1}}
\newcommand{\mestrado}[1]{\gdef\@mestrado{#1}}
\newcommand{\graduacao}[1]{\gdef\@graduacao{#1}}
\newcommand{\documento}[1]{\gdef\@documento{#1}}

\DeclareOption{ec}{\course{\ec}\graduacao{Engenheiro de Computa{\c c}{\~a}o}}
\DeclareOption{ea}{\course{\ea}\graduacao{Engenheiro de Automa{\c c}{\~a}o}}
\DeclareOption{si}{\course{\si}\graduacao{Bacharel em Sistemas de Informa{\c c}{\~a}o}}
\DeclareOption{ppgmc}{\course{\ppgmc}\mestrado{Modelagem Computacional}}
\DeclareOption{ppgcomp}{\course{\ppgcomp}\mestrado{Engenharia de Computa{\c c}{\~a}o}}

\newcommand{\nocipinfo}[1]{\gdef\@nocipinfo{#1}}
\DeclareOption{nocipinfo}{\nocipinfo{1}}

\DeclareOption{english}{\@englishtrue\OptionNotUsed}\newif\if@english
\DeclareOption{oneside}{\AtEndOfClass{\@twosidefalse}\OptionNotUsed}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions
\relax

%==============================================================================
% Herança da classe `report' e inclusão de pacotes e arquivos necessários
%==============================================================================
\LoadClass[12pt,a4paper,twoside]{report}

\RequirePackage[english,brazilian]{babel}
\RequirePackage[pdftex]{hyperref}
\RequirePackage{lastpage}
\RequirePackage{indentfirst}
\RequirePackage[square, numbers]{natbib}
\RequirePackage{chngcntr}
\RequirePackage{titletoc}
\RequirePackage{appendix}
%\RequirePackage{eso-pic}
\RequirePackage{texfurg-defs}
\RequirePackage{color}
\RequirePackage{setspace}
\RequirePackage{times}
\RequirePackage{graphicx}


\definecolor{laranjafurg}{rgb}{1,0.6,0}
\definecolor{verdefurg}{rgb}{0.09,0.7,0.44}
\definecolor{azulfurg}{rgb}{0.07,0.49,0.72}
\definecolor{cinzafurg}{rgb}{0.85,0.85,0.85}

%
% definições para textos em português
%
\@namedef{captionsbrazilian}{%
  \def\cipcaption{CIP -- CATALOGA{\c{C}}{\~A}O NA PUBLICA{\c{C}}{\~A}O}
  \def\bibname{Refer{\^e}ncias}%
  \def\abstractname{Resumo}%
  \def\appendixname{Ap{\^e}ndice}%
  \def\contentsname{Sum{\'a}rio}%
  \def\listfigurename{Lista de Figuras}%
  \def\listtablename{Lista de Tabelas}%
  \def\figurename{Figura}%
  \def\tablename{Tabela}%
  \def\advisorname{Orientador}%
  \def\coadvisorname{Co-orientador}%
  \def\collaboratorname{Colaborador}%
  \def\listabbrvname{Lista de Abreviaturas e Siglas}%
  \def\listsymbolname{Lista de S{\'\i}mbolos}%
  \def\annexname{Anexo}%
  \def\keywordsname{Palavras-chave}%
  % Projeto de Graduação %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  \def\tccname{%
    Projeto de Gradua\c{c}\~ao -- \@course%
  }%
  \def\tccspecificinfo{%
    Projeto de Gradua\c{c}\~ao apresentado ao Curso de \@course\ da
    \furg, como requisito parcial para a obten{\c{c}}{\~a}o do grau de
    \@graduacao%
  }%
  % Trabalho Individual %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  \def\tiname{Trabalho Individual (Mestrado) -- \@course}%
  \def\tispecificinfo{%
    Trabalho Individual apresentado ao \@course\ da \furg, como
    requisito parcial para a obten{\c{c}}{\~a}o do grau de Mestre em
    \@mestrado%
  }%
  % Exame de Qualificação de Mestrado
   \def\quaname{Qualifica{\c{c}}{\~a}o (Mestrado) -- \@course}%
  \def\quaspecificinfo{%
    Exame de Qualifica{\c{c}}{\~a}o de Mestrado apresentado ao \@course\ da
    \furg, como requisito parcial para a obten{\c{c}}{\~a}o do grau de
    Mestre em \@mestrado%
  }%
  % Dissertação de Mestrado %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  \def\dmname{Disserta{\c{c}}{\~a}o (Mestrado) -- \@course}%
  \def\dmspecificinfo{%
    Disserta{\c{c}}{\~a}o de Mestrado apresentada ao \@course\ da
    \furg, como requisito parcial para a obten{\c{c}}{\~a}o do grau de
    Mestre em \@mestrado%
  }%
}

\@namedef{datebrazilian}{%
  \def\monthname{%
    \ifcase\month\or%
    janeiro\or fevereiro\or mar{\c{c}}o\or abril\or maio\or junho\or
    julho\or agosto\or setembro\or outubro\or novembro\or dezembro%
    \fi%
  }%
  \def\ei@date{\@publyear}%
  % \def\ei@date{\@publmonth\ de~\@publyear}%
}

%
% definições para textos em inglês
%
\@namedef{captionsenglish}{%
  \def\cipcaption{CIP -- CATALOGA{\c{C}}{\~A}O NA PUBLICA{\c{C}}{\~A}O}
  \def\bibname{Refer{\^e}ncias}%
  \def\abstractname{Abstract}%
  \def\appendixname{Ap{\^e}ndice}%
  \def\contentsname{Sum{\'a}rio}%
  \def\listfigurename{Lista de Figuras}%
  \def\listtablename{Lista de Tabelas}%
  \def\figurename{Figura}%
  \def\tablename{Tabela}%
  \def\advisorname{Orientador}%
  \def\coadvisorname{Co-orientador}%
  \def\collaboratorname{Colaborador}%
  \def\listabbrvname{Lista de Abreviaturas e Siglas}%
  \def\listsymbolname{Lista de S{\'\i}mbolos}%
  \def\annexname{Anexo}%
  \def\keywordsname{Keywords}%
  % Trabalho de Conclusão de Curso %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  \def\tccname{%
    Projeto de Gradua\c{c}\~ao -- \@course%
  }%
  \def\tccspecificinfo{%
    Projeto de Gradua\c{c}\~ao apresentado ao \@course\ da \furg, como
    requisito parcial para a obten{\c{c}}{\~a}o do grau de \@graduacao%
  }%
  % Trabalho Individual %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  \def\tiname{Trabalho Individual (Mestrado) -- \@course}%
  \def\tispecificinfo{%
    Trabalho Individual apresentado ao \@course\ da \furg, como
    requisito parcial para a obten{\c{c}}{\~a}o do grau de Mestre em
    \@mestrado%
  }%
  % Dissertação de Mestrado %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  \def\dmname{Disserta{\c{c}}{\~a}o (Mestrado) -- \@course}%
  \def\dmspecificinfo{%
    Disserta{\c{c}}{\~a}o de Mestrado apresentada ao \@course\ da
    \furg, como requisito parcial para a obten{\c{c}}{\~a}o do grau de
    Mestre em \@mestrado%
  }%
}

\@namedef{dateenglish}{%
  \def\monthname{%
    \ifcase\month\or%
    January\or February\or March\or April\or May\or June\or July\or
    August\or September\or October\or November\or December%
    \fi%
  }%
  \def\ei@date{\@publyear}%
  % \def\ei@date{\@publmonth~\@publyear}%
}

\if@english%
\selectlanguage{english}%
\AtBeginDocument{\selectlanguage{english}}%
\fi


%==============================================================================
% Descomente para Arial
%==============================================================================
%\renewcommand*\familydefault{\sfdefault}%
%\renewcommand{\rmdefault}{phv}%
%\renewcommand{\sfdefault}{phv}

%==============================================================================
% Margens do texto
%==============================================================================
\newlength{\ei@topmargin}%
\setlength{\ei@topmargin}{30mm}%
\newlength{\ei@pagenummargin}%
\setlength{\ei@pagenummargin}{20mm}%
\newlength{\ei@bottommargin}%
\setlength{\ei@bottommargin}{20mm}%
\newlength{\ei@sidemargin}%
\setlength{\ei@sidemargin}{30mm}%
\setlength{\marginparwidth}{25mm}

% ajuste das medidas verticais
\setlength{\topmargin}{\ei@pagenummargin}
\addtolength{\topmargin}{-1em} % isto é +- a altura do núm. da página
\addtolength{\topmargin}{-1in} %
\setlength{\headheight}{1em}%
\setlength{\headsep}{\ei@topmargin}%
\addtolength{\headsep}{-\ei@pagenummargin}%
\setlength{\textheight}{\paperheight}%
\addtolength{\textheight}{-\ei@topmargin}%
\addtolength{\textheight}{-\ei@bottommargin}%
\setlength{\footskip}{\ei@bottommargin}%

% ajuste das medidas horizontais
\setlength{\oddsidemargin}{\ei@sidemargin}%
\addtolength{\oddsidemargin}{-1in}%
\setlength{\evensidemargin}{\oddsidemargin}%
\setlength{\textwidth}{\paperwidth}%
\addtolength{\textwidth}{-2\ei@sidemargin}%
\setlength{\marginparsep}{\ei@sidemargin}%
\addtolength{\marginparsep}{-\marginparwidth}%
\setlength{\marginparsep}{.5\marginparsep}

%==============================================================================
% Numeração das páginas
%==============================================================================
\def\ps@texfurg{%
  \let\@oddfoot\@empty%
  \let\@evenfoot\@empty%
  \def\@oddhead{\hspace*{\fill}{\small\thepage}}%
  \def\@evenhead{\hspace*{\fill}{\small\thepage}}%
} 

\pagestyle{empty}%
\let\ps@plain\ps@empty

%==============================================================================
% Definição de autor(es), orientador e co-orientador
%==============================================================================
\newcounter{ei@authorcount}
\renewcommand{\author}[2]{
        \addtocounter{ei@authorcount}{1}
        \expandafter\gdef\csname @author\alph{ei@authorcount}last\endcsname{#1}
        \expandafter\gdef\csname @author\alph{ei@authorcount}first\endcsname{#2}
        \expandafter\gdef\csname @author\alph{ei@authorcount}\endcsname{#2 #1}
}

\newcounter{ei@advisorcount}
\DeclareRobustCommand{\advisor}[3][]{
        \addtocounter{ei@advisorcount}{1}
        \expandafter\gdef\csname @advisor\alph{ei@advisorcount}last\endcsname{#2}
        \expandafter\gdef\csname @advisor\alph{ei@advisorcount}first\endcsname{#3}
        \expandafter\gdef\csname @advisor\alph{ei@advisorcount}\endcsname{#1~#3 #2}
}

\newcounter{ei@coadvisorcount}
\DeclareRobustCommand{\coadvisor}[3][]{
        \addtocounter{ei@coadvisorcount}{1}
        \expandafter\gdef\csname @coadvisor\alph{ei@coadvisorcount}last\endcsname{#2}
        \expandafter\gdef\csname @coadvisor\alph{ei@coadvisorcount}first\endcsname{#3}
        \expandafter\gdef\csname @coadvisor\alph{ei@coadvisorcount}\endcsname{#1~#3 #2}
}

\newcounter{ei@collaboratorcount}
\DeclareRobustCommand{\collaborator}[3][]{
        \addtocounter{ei@collaboratorcount}{1}
        \expandafter\gdef\csname @collaborator\alph{ei@collaboratorcount}last\endcsname{#2}
        \expandafter\gdef\csname @collaborator\alph{ei@collaboratorcount}first\endcsname{#3}
        \expandafter\gdef\csname @collaborator\alph{ei@collaboratorcount}\endcsname{#1~#3 #2}
}


%==============================================================================
% Definição das palavras-chave (máx. 10)
%==============================================================================
\newcounter{kwcounter}
\newcommand{\keyword}[1]{
        \addtocounter{kwcounter}{1}
        \expandafter\gdef\csname keyw\alph{kwcounter}\endcsname{#1}
}

\newcommand{\@cipkw}{%
        \@ifundefined{keywa}{}{1.~\expandafter\MakeUppercase\keywa\@. }%
        \@ifundefined{keywb}{}{2.~\expandafter\MakeUppercase\keywb\@. }%
        \@ifundefined{keywc}{}{3.~\expandafter\MakeUppercase\keywc\@. }%
        \@ifundefined{keywd}{}{4.~\expandafter\MakeUppercase\keywd\@. }%
        \@ifundefined{keywe}{}{5.~\expandafter\MakeUppercase\keywe\@. }%
        \@ifundefined{keywf}{}{6.~\expandafter\MakeUppercase\keywf\@. }%
        \@ifundefined{keywg}{}{7.~\expandafter\MakeUppercase\keywg\@. }%
        \@ifundefined{keywh}{}{8.~\expandafter\MakeUppercase\keywh\@. }%
        \@ifundefined{keywi}{}{9.~\expandafter\MakeUppercase\keywi\@. }%
        \@ifundefined{keywj}{}{10.~\expandafter\MakeUppercase\keywj\@. }%
}

\newcommand{\@abstractkw}{%
        \@ifundefined{keywa}{}{\expandafter\MakeUppercase\keywa}%
        \@ifundefined{keywb}{}{, \keywb}%
        \@ifundefined{keywc}{}{, \keywc}%
        \@ifundefined{keywd}{}{, \keywd}%
        \@ifundefined{keywe}{}{, \keywe}%
        \@ifundefined{keywf}{}{, \keywf}%
        \@ifundefined{keywg}{}{, \keywg}%
        \@ifundefined{keywh}{}{, \keywh}%
        \@ifundefined{keywi}{}{, \keywi}%
        \@ifundefined{keywj}{}{, \keywj}%
}

%==============================================================================
% Redefinição da data (para ter mês e ano separados)
%==============================================================================
\renewcommand{\date}[2]{
        \gdef\@publmonth{#1}
        \gdef\@publyear{#2}
}
\date{\monthname}{\number\year}

%==============================================================================
% Definição padrão da folha de rosto.
% Os dados específicos do tipo de trabalho (dissertação, tese, etc.) são
% informados definindo-se o comando \titlepagespecificinfo. Veja os
% arquivos .def incluídos com a classe.
%==============================================================================

\newlength{\titlepagewinwidth}\setlength{\titlepagewinwidth}{95mm}
\newlength{\titlepagewinheight}\setlength{\titlepagewinheight}{64mm}
\newlength{\titlepagewinvoffset}\setlength{\titlepagewinvoffset}{112mm}

\newcommand{\location}[2]{
        \gdef\@city{#1}
        \gdef\@state{#2}
}

\location{Rio Grande}{RS}

\renewcommand{\maketitle}{
  \begin{titlepage}
    \thetitlepage
  \end{titlepage}
  \clearpage
  \setcounter{page}{2}
}


\newcommand{\thetitlepage}{%
  \noindent%
  \parbox[b]{\textwidth}{%
    \centering% 
      \centering%
      \begin{flushleft}
			\includegraphics[scale=0.12]{./logos/furg.png}
			\hfill
			 \includegraphics[scale = 0.15]{./logos/C3.png}\\
		\end{flushleft}	
      \vskip 1cm%
      \MakeUppercase{\large{\furg}}\\[.2cm]%
      \MakeUppercase{\large{\ctres}}\\[.2cm]%
      \@ifundefined{@graduacao}{\MakeUppercase{\@course}\\[.2cm]\MakeUppercase{Curso
          de Mestrado em \@mestrado}}{\MakeUppercase{Curso de
          \@course}}\\%
      \vskip 3cm%
      \@ifundefined{@documento}{{\large Relat{\'o}rio de Trabalho Individual}}{{\large\@documento}}\\%
      \vskip 3cm%
      {\Large\textbf{\@title}}
      \vskip 1cm%
      \@authora\\
      \@ifundefined{@authorb}{}{\@authorb\\}%
      \@ifundefined{@authorc}{}{\@authorc\\}%
      \@ifundefined{@authord}{}{\@authord\\}%
  }
  \vskip 2cm%
  \@ifundefined{titlepagespecificinfo}{}{%
    \hspace*{\fill}\makebox[.5\textwidth][l]{%
      \parbox[b]{8.5cm}{%
        \titlepagespecificinfo%
      }%
    }%
    \vfill%
  }%
  \vfill%
  \@ifundefined{@advisora}{}{%
  \parbox[b]{\textwidth}{%
    \centering%
      \begin{tabular}{rp{9cm}}%
        \@ifundefined{@advisora}{}{
          \@ifundefined{@advisorb}{\advisorname:}{\advisorname es:} &
          \@ifundefined{@advisora}{}{\@advisora\\}
          \@ifundefined{@advisorb}{}{\ &}
          \@ifundefined{@advisorb}{}{\@advisorb\\}
          \@ifundefined{@advisorc}{}{\ &}
          \@ifundefined{@advisorc}{}{\@advisorc\\}
          \@ifundefined{@advisord}{}{\ &}
          \@ifundefined{@advisord}{}{\@advisord\\}}
        \@ifundefined{@coadvisora}{}{
          \@ifundefined{@coadvisorb}{\coadvisorname:}{\coadvisorname
            es:} & \@ifundefined{@coadvisora}{}{\@coadvisora\\}
          \@ifundefined{@coadvisorb}{}{\ &}
          \@ifundefined{@coadvisorb}{}{\@coadvisorb\\}
          \@ifundefined{@coadvisorc}{}{\ &}
          \@ifundefined{@coadvisorc}{}{\@coadvisorc\\}
          \@ifundefined{@coadvisord}{}{\ &}
          \@ifundefined{@coadvisord}{}{\@coadvisord\\}}
        \@ifundefined{@collaboratora}{}{
          \@ifundefined{@collaboratorb}{\collaboratorname:}{\collaboratorname
            es:} & \@ifundefined{@collaboratora}{}{\@collaboratora\\}
          \@ifundefined{@collaboratorb}{}{\ &}
          \@ifundefined{@collaboratorb}{}{\@collaboratorb\\}
          \@ifundefined{@collaboratorc}{}{\ &}
          \@ifundefined{@collaboratorc}{}{\@collaboratorc\\}
          \@ifundefined{@collaboratord}{}{\ &}
          \@ifundefined{@collaboratord}{}{\@collaboratord\\}}
        \end{tabular}
      }%
    \vfill%
    \vfill%
  }%
  \centerline{\@city, \ei@date}%
}

%==============================================================================
% Ajuste do sumário (nada indentado) 
%==============================================================================
\newlength{\ei@chapnumindent}\setlength{\ei@chapnumindent}{1.8em}

%\renewcommand*{\l@chapter}[2]{
%        \addpenalty{-\@highpenalty}
%        \vskip -1ex \@plus\p@
%        \setlength\@tempdima{1.5em}
%        \begingroup
%        \parindent \z@ \rightskip \@pnumwidth
%        \parfillskip -\@pnumwidth
%        \leavevmode\bfseries\sffamily
%        \advance\leftskip\@tempdima
%       \hskip -\leftskip
%        \@dottedtocline{0}{0em}{\ei@chapnumindent}{\MakeUppercase{#1}}{#2}
%        \penalty\@highpenalty 
%        \endgroup
%}
\renewcommand*{\l@section}[2]
              {\@dottedtocline{1}{0em}{2.8em}{\textbf{#1}}{\hss #2}}
\renewcommand*{\l@subsection}{\@dottedtocline{2}{0em}{3.7em}}
 
\newif\if@aftertoc
\@aftertocfalse
\renewcommand{\tableofcontents}{%
        \chapter*{\contentsname}
        \@starttoc{toc}\@aftertoctrue
}


%==============================================================================
% Definição das listas de abreviaturas e siglas e de símbolos
%==============================================================================
\newenvironment{listofabbrv}[1]{
  \chapter*{\listabbrvname}
  \begin{list}{\textbf{??}}{%
      \settowidth{\labelwidth}{#1}%
      \setlength{\labelsep}{1em}%
      \setlength{\itemindent}{0mm}%
      \setlength{\leftmargin}{\labelwidth}%
      \addtolength{\leftmargin}{\labelsep}%
      \setlength{\rightmargin}{0mm}%
      \setlength{\itemsep}{.1\baselineskip}%
      \renewcommand{\makelabel}[1]{\makebox[\labelwidth][l]{##1}}%
    }
  }{
  \end{list}
} 

\newenvironment{listofsymbols}[1]{
  \chapter*{\listsymbolname}
  \begin{list}{\textbf{??}}{%
      \settowidth{\labelwidth}{#1}%
      \setlength{\labelsep}{1em}%
      \setlength{\itemindent}{0mm}%
      \setlength{\leftmargin}{\labelwidth}%
      \addtolength{\leftmargin}{\labelsep}%
      \setlength{\rightmargin}{0mm}%
      \setlength{\itemsep}{.1\baselineskip}%
      \renewcommand{\makelabel}[1]{\makebox[\labelwidth][l]{##1}}%
    }
  }{
  \end{list}
}

%==============================================================================
% Resumo (abstract) e Abstract (englishabstract)
%==============================================================================
\renewenvironment{abstract}{%
  \chapter*{\abstractname}
  \@ifundefined{@nocipinfo}{
  \noindent{\MakeUppercase{\@authoralast}, \@authorafirst. \textbf{\@title}. {\@publyear}. \pageref{LastPage}~f. \@cipspecificinfo. {\furg}, {\@city}.}\\~\\}{}
}{%
  \par\vfill
  \noindent\textbf{\keywordsname:} \@abstractkw.
}

\newenvironment{englishabstract}[2]{%
  \if@openright\cleardoublepage\else\clearpage\fi%
  \gdef\@englishkeywords{#2}%
  \gdef\@englishtitle{{#1}}%
  \iflanguage{english}{
    \begin{otherlanguage}{brazilian}
    }{
      \begin{otherlanguage}{english}
      }

      \chapter*{\abstractname}
      \noindent{\MakeUppercase{\@authoralast}, \@authorafirst. \textbf{\@englishtitle}. {\@publyear}. \pageref{LastPage}~f. \@cipspecificinfo. {\furg}, {\@city}.}\\~\\
    }{
      \par\vfill
      \noindent\textbf{\keywordsname:} \@englishkeywords.
    \end{otherlanguage}
}

%==============================================================================
% Formatação dos capítulos.
% Os comandos \@chapter e \@schapter são redefinidos para que a
% numeração de páginas seja correta (deve aparecer somente a partir do
% primeiro capítulo do texto, mas não nas páginas iniciais de
% capítulos).
% Os comandos \@makechapterhead e \@makeschapterhead fazem a
% formatação dos títulos propriamente ditos.
%==============================================================================
\newcommand{\ei@chapterfont}{\@setfontsize\Large{16}{20}}
\def\@chapapp{}

\def\@chapter[#1]#2{%
	\onehalfspacing
  \refstepcounter{chapter}%
  \addcontentsline{toc}{chapter}{\protect\numberline{\@chapapp\thechapter}#1}%
  \addtocontents{lof}{\protect\addvspace{10\p@}}%
  \addtocontents{lot}{\protect\addvspace{10\p@}}%
  \pagestyle{texfurg}\let\ps@plain\ps@texfurg%
  \@makechapterhead{#2}\@afterheading%
}

\def\@makechapterhead#1{%
  \vspace*{90pt}%
  \reset@font\noindent{\ei@chapterfont\sffamily\textbf{\@chapapp\thechapter\hspace{1em}\MakeUppercase{#1}}\par}%
  \addvspace{42pt}%
  \thispagestyle{empty}%
}

\def\@schapter#1{%
  \if@aftertoc\addcontentsline{toc}{chapter}{#1}\fi%
  \addtocontents{lof}{\protect\addvspace{10\p@}}%
  \addtocontents{lot}{\protect\addvspace{10\p@}}%
  \@makeschapterhead{#1}\@afterheading%
}

\def\@makeschapterhead#1{%
  \vspace*{90pt}%
  \reset@font\centerline{\ei@chapterfont\sffamily\textbf{\MakeUppercase{#1}}}%
  \addvspace{42pt}%
}

\renewcommand{\appendix}[1][\appendixname]{%
  \setcounter{chapter}{0}%
  \renewcommand{\thechapter}{\Alph{chapter}}%
  \setcounter{tocdepth}{0}%
  \@captionlistingfalse%
  %\gdef\@chapapp{\MakeUppercase{#1}\space}%
  \addtocontents{toc}{%
  {\bigskip\medskip\noindent%
  \textbf{ANEXOS}\par}
   \settowidth{\ei@chapnumindent}{{\sffamily\textbf{\@chapapp}}}%
    \addtolength{\ei@chapnumindent}{1.8em}%
  }%
}

\newcommand{\annex}{\appendix[\annexname]}

%==============================================================================
% Formatação das seções
%==============================================================================
\setcounter{secnumdepth}{4} 

\renewcommand{\section}{%
  \@startsection{section}{1}{0pt}{18pt}{9pt}{\reset@font\large\bfseries}
} 

\renewcommand{\subsection}{%
  \@startsection{subsection}{2}{0pt}{12pt}{6pt}{\reset@font\bfseries}
} 

\renewcommand{\subsubsection}{%
  \@startsection{subsubsection}{3}{0pt}{12pt}{6pt}{\reset@font\itshape}
} 

\renewcommand{\paragraph}{%
  \@startsection{paragraph}{4}{0pt}{12pt}{6pt}{\reset@font} 
}

\renewcommand{\subparagraph}{%
  \@startsection{subparagraph}{5}{0pt}{1ex}{-1em}{\reset@font\bfseries}
}

%==============================================================================
% Formatação das legendas
%==============================================================================
\renewcommand{\thefigure}{\@arabic\c@figure}
\renewcommand{\thetable}{\@arabic\c@table}

\counterwithout{figure}{chapter}
\counterwithout{equation}{chapter}
\counterwithout{table}{chapter}

%==============================================================================
% Redefinição do conteúdo das listas de figuras e tabelas
%==============================================================================
\newif\if@captionlisting\@captionlistingtrue
\long\def\@caption#1[#2]#3{%
  \par
  \if@captionlisting%
    \addcontentsline{\csname ext@#1\endcsname}{#1}%
        {\protect\numberline{\csname fnum@#1\endcsname}{\ignorespaces #2}}%
  \fi%
  \begingroup
    \@parboxrestore
    \if@minipage
      \@setminipage
    \fi
    \normalsize
    \@makecaption{\csname fnum@#1\endcsname}{\ignorespaces #3}\par
  \endgroup%
}

\renewcommand*{\l@figure}{\@dottedtocline{1}{0em}{5.5em}}
\let\l@table\l@figure

%==============================================================================
% Redefinição do formato de citações longas
%==============================================================================
\renewenvironment{quote}{%
  \small%
  \begin{list}{}{\setlength{\leftmargin}{40mm}\item\relax}
  }{%
  \end{list}
}

%==============================================================================
% Ajuste do formato das citações e referências
%==============================================================================
\setlength{\bibhang}{0pt}
\let\cite\citep

\newcounter{excounter}

\newcommand{\examiner}[1]{%
  \addtocounter{excounter}{1}%
  \expandafter\gdef\csname examiner\alph{excounter}\endcsname{#1}%
}

\newcommand{\linespace}{%
  ~\\~\\~\\~\\~\\\hline%
}

\newcommand{\@allexaminers}{%
  \@ifundefined{examinera}{}{\linespace\examinera}%
  \@ifundefined{examinerb}{}{\linespace\examinerb}%
  \@ifundefined{examinerc}{}{\linespace\examinerc}%
  \@ifundefined{examinerd}{}{\linespace\examinerd}%
  \@ifundefined{examinere}{}{\linespace\examinere}%
  \@ifundefined{examinerf}{}{\linespace\examinerf}%
  \@ifundefined{examinerg}{}{\linespace\examinerg}%
  \@ifundefined{examinerh}{}{\linespace\examinerh}%
  \@ifundefined{examineri}{}{\linespace\examineri}%
  \@ifundefined{examinerj}{}{\linespace\examinerj}%
}

\newcommand{\makeexaminers}{%
  \clearpage%
  \begin{flushleft}
			\includegraphics[scale=0.12]{./logos/furg.png}
			\hfill
			 \includegraphics[scale = 0.15]{./logos/C3.png}\\
  \end{flushleft}	
    \vskip 1cm%
   % \centering
   \@ifundefined{@documento}{{\large Relat{\'o}rio de Trabalho Individual}}{{\large\@documento}}\\%
   \vskip 1cm%      
    {\Large\textbf{\@title}}
    \vskip 1cm%
    \@authora\\
      \@ifundefined{@authorb}{}{\@authorb\\}%
      \@ifundefined{@authorc}{}{\@authorc\\}%
      \@ifundefined{@authord}{}{\@authord\\}%
    
    \vskip 1cm%

  \mbox{}%
  \vskip 4cm%
  %\vfill%
  \noindent\textbf{Banca examinadora:}\\
  \begin{tabular}{l}
    \@allexaminers
  \end{tabular}
}

\newcommand{\makecover}{%
	\singlespacing
\thispagestyle{empty}
  \clearpage%
  \mbox{}%
  \vfill%
  \fcolorbox{black}{white}{%
  \parbox[b]{14cm}{%
    \begin{minipage}{1.8cm}
\rotatebox{90}{~\parbox{12cm}{%
    \begin{minipage}[c]{1cm}
            \includegraphics[width=\columnwidth]{furgw}
    \end{minipage}\hfill
    \begin{minipage}[c]{10.5cm}
\textbf{\@title} -- \@authora
    \end{minipage}
}~}
    \end{minipage}
    \begin{minipage}{14cm}
  \noindent%
  \fcolorbox{black}{laranjafurg}{%
    \parbox[b]{12cm}{%
      \begin{center}
      \MakeUppercase{\textbf{\furg}}\\%
      \ctres\\%
      \@ifundefined{@course}{{\ppgcomp}}{\large{Curso de \@course}}\\%
      \includegraphics[width=3cm]{furg}\\
      \@ifundefined{@course}{{Disserta{\c{c}}{\~a}o}}{{Trabalho Acad{\^e}mico}}%
    \end{center}
}%
  }%
  \vskip .2cm%
  \noindent%
  \fcolorbox{black}{azulfurg}{%
    \parbox[c][2cm]{12cm}{%
      \begin{center}
\vfill 
     {\color{white}\textbf{\@title}}%
\vfill 
    \end{center}
}%
  }%
  \vskip .2cm%
  \noindent%
  \fcolorbox{black}{verdefurg}{%
    \parbox[c][2cm]{12cm}{%
      \begin{center}
      {\textbf{\MakeUppercase{\@authora}\\
      \@ifundefined{@authorb}{}{\MakeUppercase{\@authorb}\\}%
      \@ifundefined{@authorc}{}{\MakeUppercase{\@authorc}\\}%
      \@ifundefined{@authord}{}{\MakeUppercase{\@authord}\\}}}%
\end{center}
}%
  }%
  \vskip .2cm%
  \noindent%
  \fcolorbox{black}{cinzafurg}{%
    \parbox[b]{12cm}{%
      \centering%
      \@city, \ei@date%
    }%
    }%
  \end{minipage}}
    }
\vfill
}


\newenvironment{agradecimentos}{%
  \chapter*{Agradecimentos}%
}{%
}

\newenvironment{dedicatoria}{%
  \clearpage%
  \em\itshape%
  \mbox{}\vfill\begin{flushright}%
  }{%
  \end{flushright}%
}

\newenvironment{epigrafe}{%
  \clearpage%
  \sffamily\itshape%
  \mbox{}\vfill\begin{flushright}%
  }{%
  \end{flushright}%
}

%ficha catalográfica
\newcommand{\makecippage}{%
        \clearpage%
\mbox{}\vfill
\noindent Dados de cataloga\c{c}\~{a}o na fonte:\\
\noindent \@nomebibliotecario\\
\noindent \@nomebiblioteca\\
\vskip  1cm
        \begin{center}
                \texfurg@cipwindow
        \end{center}
        \vfill\mbox{}
%        \nominata
}

% definição do quadro
\def\texfurg@cipwindow{%
        \framebox[140mm]{%
        \begin{minipage}[t]{20mm}% 
                \vskip .3cm
 \@codigocip
        \end{minipage}%
        \begin{minipage}[t]{110mm}%
                \vspace*{0.2ex}
                \setlength{\parindent}{1.5em}%
                \setlength{\parskip}{1.3ex}%
                \noindent\@authoralast, \@authorafirst\par
                \@title\ / \@authora.\ -- \@city, \@publyear. --
                \pageref{LastPage}~f: gr\'{a}f. --
                \@cipspecificinfo. \furg. \ctres. \@city,
                \@publyear. -- Orientador \@advisorafirst\ \@advisoralast
                \@ifundefined{@coadvisorafirst}{.}{; Co-orientador
                  \@coadvisorafirst\ \@coadvisoralast.} \par
                \@cipkw I.~\@advisoralast,
                \@advisorafirst. \@ifundefined{@coadvisorafirst}{II.~T\'{\i}tulo.}{II.~\@coadvisoralast,
                  \@coadvisorafirst. III.~T\'{\i}tulo.}
                \begin{flushright}
                  CDD: \@codigocdd
                \end{flushright}
                \vspace{0.4ex}
        \end{minipage}%
        }%
}
