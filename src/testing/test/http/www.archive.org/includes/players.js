////////////////////////////////////////////////////////////////////////////////
//Copyright(c)2005-(c)2008 Internet Archive. Software license GPL version 2.


/* TODOS:
 xxxx  IE body getAttribute('class') not working
   
 xxx   players.js?id2insertInto=...&identifier=...
 xxx   window.onload() (runs any prior onload() setting they had at end?!)
 xxx   make movies.server null for external users and use /download/ in that case
 xxx   about/flash.php embedding help w/ playlists?!
 xxx   [grep below]
*/




// encrapsulate all our functions and variables.  no globals!
var IAPlay = {

// constants
CLIK2PLAYWIDTH:320,
CONTROLLER_HEIGHT:28,
// why do flash use commas, why?
MIN_FLASH_VERSION:"7,0,0",   // the bare minimum -- a C- student
MP4_FLASH_VERSION:"9,0,115", // this one can play h.264-encoded .mp4!

// usually constant, but *can* change
FLASH_WIDTH:320,  // or 640 for h.264 clips
VIDEO_HEIGHT:240, // or 480 for h.264 clips


  

// variable that holds the player API. it is initially null 
flowplayer:null,

// what clip position in the playlist is the player at?
clipNum:0,

// object that holds movies playlist info and other stuff
movies:null,


// makes browser load other CSS and other JS files we need.
// sets up "onload" to insert the flash player
setup:function()
{
  var headobj = document.getElementsByTagName("head")[0];         

  var obj = document.createElement('script');
  obj.setAttribute('type','text/javascript');
  obj.setAttribute('src', '/flow/html/flashembed.min.js');
  headobj.appendChild(obj);

  var obj = document.createElement('script');
  obj.setAttribute('type', 'text/javascript');
  obj.setAttribute('src' , '/flow/AC_OETags.js');
  headobj.appendChild(obj);

  var obj = document.createElement('link');
  obj.setAttribute('type', 'text/css');
  obj.setAttribute('href', '/stylesheets/players.css');
  obj.setAttribute('rel' , 'stylesheet');
  headobj.appendChild(obj);

  window.onload = function() { IAPlay.insertPlayer(); };
},


////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
//
//     MOVIES and AUDIO
//
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
updateTable:function()
{
  // if playlist present, show the clip's "play triangle" icon; hide the rest
  var fp = document.getElementById("fplaylist");
  if (!fp)
    return;
  
  var els = fp.getElementsByTagName("img");
  for (var i=0; i < els.length; i++)
    els[i].style.visibility = (i==this.clipNum ? 'visible':'hidden');
},


  
// arg is overloaded 3 ways:
//  - undefined, from onload, for audio or movies XSL
//  - JSON object for movies when user has clicked through "click to play"
//  - string for "flash.php" user embedding help
insertPlayer:function(arg)
{
  // see if we are a movie
  var el = document.getElementsByTagName('body')[0];
  var movie = (el.getAttribute('class') == 'Movies');//xxxxx always false in IE!

  if (!document.getElementById("flowplayerdiv"))
    return false;//xxx noop for now -- for live site until cutover!  then later alert() for 3rd party peeps
  
                                           
  if ('undefined' == typeof arg)
  {
    // called due to XSL page being loaded, eg:
    //    www.archive.org/stylesheets/sound.xsl
    //    www.archive.org/stylesheets/movies.xsl
    var bedarg = document.getElementById('bedarg').value;

    if (movie)
    {
      //console.log(bedarg);
      this.movies = eval('['+bedarg+']'); this.movies = this.movies[0]; //xxx not sure why have to do this!
      
      return this.click2play();
    }
  }
  else if ('string' == typeof arg)
  {
    movie = false;
  }
  
  
  
  if (!movie)
  {
    if (!this.versionOK(this.MIN_FLASH_VERSION, 0))
      return false;

    arg = eval(bedarg); // string to JSON
  //console.log(arg);
  }


  /************* THE PLAYLIST ***************/ 
  var playListObj = [];

  
  var table = '<table width="100%" border="1" class="sleek">\n';
  for (var i=0, obj; obj=arg[i]; i++)
  {
    playListObj[i] = {'url': obj.url};

    table +=
      "<tr class=\"" + (i%2 ? 'eve' : 'odd') +
      "\"><td class=\"c1\">"+(i+1)+"<img src=\"/images/orange_arrow.gif\"/></td>"+
      '<td><a idx="'+i+'" href="'+obj.url+'">'+obj.name+"</a></td>"+
      (typeof(obj.length)=="undefined"?"":"<td class=\"c3\">"+obj.length+"</td>")+
      "</tr>\n";
  }
  table += "</table>\n";
  //console.log(table);


  var fplaylist = document.getElementById("fplaylist");
  if (fplaylist)
  {
    fplaylist.innerHTML = table;
    
  
    // find all links within div#fplaylist and customize their onClick event
    var links = fplaylist.getElementsByTagName("a");  
    for (var i=0; i < links.length; i++)
    {
      // in case 3rd party user/site made their own links in the fplaylist id,
      // let's use them instead of the ones we set up above!
      playListObj[i] = {'url': links[i].getAttribute("href")};
      
      links[i].onclick = function()
        {
          var idx = this.getAttribute("idx");
          
          IAPlay.clipNum = idx;//xxx would be nice if "i" worked, then could scrap idx=".."
          //console.log("CLICK TO: "+IAPlay.clipNum);
          IAPlay.flowplayer.ToClip(IAPlay.clipNum); //NOTE: this fires an onClipChanged()
          
          return false; // disable link's default behaviour 
        }
    }
  }

  //console.log(playListObj);

  if (!movie)
    document.getElementById("flowplayerdiv").style.height=this.CONTROLLER_HEIGHT;


  // create Flowplayer instance into DIV element whose id="flowplayerdiv" 
  // Flash API is automatically returned.
  this.flowplayer = flashembed(
    "flowplayerdiv",
    /**/{src:"/flow/FlowPlayerLight.swf", bgcolor:'ffffff'},
    /**/{config:{controlBarBackgroundColor: '0x000000',
                 loop:                  false,
                 showVolumeSlider:      true, 
                 controlBarGloss:       'high',
                 playList:              playListObj,
                 showPlayListButtons:   true,
                 usePlayOverlay:        false,
                 menuItems:             [false,false,false,false,true,true,false],
                 initialScale:          (movie?'fit':'scale'),
                 autoPlay:              (movie?true:false),
                 autoBuffering:         (movie?true:false),
                 showMenu:              (movie?true:false),
                 showMuteVolumeButton:  (movie?true:false), 
                 showFullScreenButton:  (movie?true:false)
      }});
  

},

  

// parses a CGI arg
arg:function(theArgName)
{
  sArgs = location.search.slice(1).split('&');//xxx this is like /details/movies -- not OUR url!
  
  r = '';
  for (var i=0; i < sArgs.length; i++)
  {
    if (sArgs[i].slice(0,sArgs[i].indexOf('=')) == theArgName)
    {
      r = sArgs[i].slice(sArgs[i].indexOf('=')+1);
      break;
    }
  }
  return (r.length > 0 ? unescape(r).split(',') : '')
},






  
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
//
//     MOVIES
//
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
insertPlayerWrapper:function()
{
  identifier = this.movies.identifier;

  
  
  if (!this.movies.flvs  &&  !this.movies.mp4s)
    return false;
  
  if (!this.versionOK(this.MIN_FLASH_VERSION, 1))
    return false;
  // we've detected an acceptable version -- embed Flash Content SWF
    
  
  var PLAYLIST = null;
  if (this.movies.mp4s.length  &&  this.versionOK(this.MP4_FLASH_VERSION, 0))
  {
    // latest flash plugin that can handle h.264 mp4s!
    
    // there are mp4s!  keep only the mp4s
    PLAYLIST = this.movies.mp4s;
    
    // quadruple the video playsize (double width; double height)
    this.FLASH_WIDTH = 640;
    this.VIDEO_HEIGHT = 480;
  }
  else if (this.movies.flvs.length)
  {
    // flash plugin can only handle flash video (and shockwave) clips
    PLAYLIST = this.movies.flvs;
  }


  if (!PLAYLIST)
  {
    document.getElementById("flowplayerdiv").innerHTML =  'Sorry!  no clips in this item could be played with your flash plugin.';
    return false;
  }
  //console.log(PLAYLIST);

  

  // set "flowplayerdiv" width and height (flowplayer flash obj maximizes into it)
  var el = document.getElementById("flowplayerdiv");
  el.style.height = (this.VIDEO_HEIGHT + this.CONTROLLER_HEIGHT);
  el.style.width =  this.FLASH_WIDTH;

  var el = document.getElementById("fplaylist");
  if (el)
    el.style.width =  this.FLASH_WIDTH;

  this.insertPlayer(PLAYLIST);
},




click2play:function()
{
  if (navigator.userAgent.indexOf('iPhone') >= 0  ||
      navigator.userAgent.indexOf('iPod'  ) >= 0)
  {
    // the HTTP user agent appears to be an iphone -- don't bother with the
    // flash video and have the click go right to a MPEG4 instead...
    // (... or the agent appears to be an ipod video 8-)
    clik = '<a href="/download/' + IAPlay.movies.identifier + '/format=' +
      (mp4count > 0 ? 512 : 256)+'Kb%20MPEG4">';
  }
  else
  {
    clik =
    '<a href="/about/javascript-required.htm" '+
    ' onClick="IAPlay.insertPlayerWrapper(); return false;">';
  }

  str =
    '<div style="width:'+IAPlay.CLIK2PLAYWIDTH+'; height: 240px; text-align:center; position:relative;">' +
    '<div style="width:'+IAPlay.CLIK2PLAYWIDTH+'; position:absolute; top:0; left:0;">';

  //console.log(IAPlay.movies);
  var thumbs=IAPlay.movies.thumbs;
  
  var l=thumbs.length;
  /**/ if (l==1)thumbA2 = new Array(thumbs[0], null,      null,      null);
  else if (l==2)thumbA2 = new Array(thumbs[0], null,      null,      thumbs[1]);
  else if (l==3)thumbA2 = new Array(thumbs[0], thumbs[1], thumbs[2], null);
  else if (l>=4)thumbA2 = new Array(thumbs[0], thumbs[1], thumbs[2], thumbs[3]);
  else          thumbA2 = new Array(null,      null,      null,      null);
    
        
  // show up to first 4 thumbs, in 2x2 grid
  // add 10px solid black bar on top and bottom of overall grid
  for (i=0; i < 4; i++)
  {
    str +=
      clik +
      '<img alt="click to play movie" title="click to play movie" style="border:0; border'+
      (i < 2 ? '-top' : '-bottom') +
      ':10px solid black; width:160px; height:110px;" ' +
      (thumbA2[i] ?
       'src="http://'+ IAPlay.movies.server + thumbA2[i] + '"/>' :
       'src="/images/movies.gif">') +
      '</a>';
    if (i % 2 == 1)
      str += '<br/>';
  }

  
  str +=
    clik +
    '<img alt="click to play movie" title="click to play movie" style="position:absolute; top:0px; left:0px; height:240px; width:'+IAPlay.CLIK2PLAYWIDTH+'px; z-index:2; border:0px;" src="/images/clicktoplay.png"/></a>';

  
  str += '</div></div>';
  //console.log(str);
  
  document.getElementById("flowplayerdiv").innerHTML = str;
},
  


versionOK:function(versionStr, writeMessageNotOK)
{
  // Check to see if the version meets the requirements for playback
  var pieces = versionStr.split(",");
  
  var requiredMajorVersion = pieces[0];
  var requiredMinorVersion = pieces[1];
  var requiredRevision     = pieces[2];
  
  // Version check based on Major version+ of Flash required
  var hasReqestedVersion = DetectFlashVer(requiredMajorVersion,
                                          requiredMinorVersion,
                                          requiredRevision);

  if (!hasReqestedVersion)
  {  // flash is too old or we can't detect the plugin
    if (writeMessageNotOK)
    {
      document.getElementById("flowplayerdiv").innerHTML =
        '<div style="padding:10px; border:1px solid brown; background-color:wheat;" class="urge">'
        +'Internet Archive\'s<!--\'--> in-browser video player '
        +(versionStr==this.MP4_FLASH_VERSION ? ' (now featuring latest h.264 video) ' : '')
        +'requires '
        +'Adobe Flash Player version ' + versionStr + ' or higher. '
        +'It appears that you do not have it installed.<br/>'
        +'<a href="http://www.adobe.com/go/getflash/">Get current Flash version</a></div>';
    }
    return false;
  }

  return true;
}
  

}; // end IAPlay definition







   


// flowplayer API callback that we implement to get flash events when they happen
function onClipChanged(clip)
{
  IAPlay.clipNum = IAPlay.flowplayer.getCurrentClip();
  //console.log("CLIP CHANGED: "+IAPlay.clipNum);
  IAPlay.updateTable();
}


// flowplayer API callback that we implement to get flash events when they happen
function onFlowPlayerReady()
{
  //console.log("READY: "+IAPlay.clipNum);
  IAPlay.updateTable();
}




// SET IT ALL UP!!
IAPlay.setup(); 
