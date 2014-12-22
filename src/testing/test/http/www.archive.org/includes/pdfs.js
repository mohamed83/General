// used by /stylesheets/texts.xsl
// for microfilm books with many months of newspapers in PDF



// input is an array-as-string, each logical element is like (w/o quotes):
//    "page(s);day;month"
// eg:
//    "1,2,3;17;11"
// and each element is delineated with a "|" character
function drawy(identifier, pageStr)
{
  var pageAry = pageStr.split("|");
  
  var str='';
  var lastmonth=666;
  var urlstart = 'http://www.archive.org/download/'+identifier+
    '/'+identifier+'_pdf.zip/'+identifier+'_pdf/'+identifier+'_';
  //alert(urlstart);
  
  for (i=0; i < pageAry.length; i++)
  {
    var parts    = pageAry[i].split(";");
    var pages    = parts[0].split(",");
    var day      = parts[1];
    var month    = parts[2];
    var skip_day = false;
    if (month != lastmonth)
    {
      /**/ if (month== 1) monthName=("January");
      else if (month== 2) monthName=("February");
      else if (month== 3) monthName=("March");
      else if (month== 4) monthName=("April");
      else if (month== 5) monthName=("May");
      else if (month== 6) monthName=("June");
      else if (month== 7) monthName=("July");
      else if (month== 8) monthName=("August");
      else if (month== 9) monthName=("September");
      else if (month==10) monthName=("October");
      else if (month==11) monthName=("November");
      else if (month==12) monthName=("December");
      else if (month===undefined) monthName=("Single Page PDFs");
      else /*          */ monthName=("Unknown_" + month);

      // make header/a that shows/hides a hidden div after it with the
      // month's data
      str +=
        (str == '' ? '' : '</div><!--mo--><br/>')+
        '<a href="" onclick="return tog(\'m'+month+
        '\')">+<img src="/images/folder.png"/> <u>'+monthName+'</u></a>'+
        '<div class="mo" id="m'+month+'">';
    }

    // make header/a that shows/hides a hidden div after it with the page data
    if ((day===undefined)||(day=='')) skip_day=true;
    if (skip_day) {
      str += '<div class="day">';
    } else {
      str += '<div class="day"><a href="" onclick="return tog(\'m'+month+
        'd'+day+'\')">+<img src="/images/folder.png"/> <u>'+day+
        '</u></a> <div class="pages" id="m'+month+'d'+day+'">';
    }

    // drop in the individual page links

    var offset = 1,page,pnum;
    for (j=0; j < pages.length; j++)
    {
      page = pages[j];
      if (!page)
        continue;
      if (offset>0) offset=1-page;
      pnum=parseInt(page)+offset;

      // left 0-pad to 4 digits as needed
      page = '0000'+page;
      page = page.substr(page.length-4, 4);
      
      var url = urlstart + page + '.pdf';
      str += '<a href="'+url+'">['+pnum+']</a> ';
    }

    if (skip_day) {
      str += '</div>';
    } else {
      str += '</div><!--pages-->' + '</div><!--day-->';
    }

    lastmonth = month;
  }

  str += '</div><!--mo-->';
  
  // replace the "pdfs" empty div with our hefty HTML
  var o=document.getElementById('pdfs');
  //alert(str);
  o.innerHTML = str;
  return false;
}

// makes a hidden div become visible; makes a visible div become hidden
function tog(id)
{ 
  var o=document.getElementById(id);
  if (o.style.display=='block')
    o.style.display='none';
  else
    o.style.display='block';
  return false;
}
