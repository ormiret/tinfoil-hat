import sugar, json, strformat, karax/kajax, uri, times, options

include karax/prelude

type FOI = object
  title, link, status, wdtk_id, body_id : string
  tags : seq[string]
  last_updated_at, initial_request_at: Option[DateTime]

var FOIs : seq[FOI]
var res = buildHtml:
  tdiv(class="loading"):
    text "loading..."
  
proc loadFOIs(httpStatus: int, resp: cstring) =
  let FOIj = parseJson($resp)
  let isoFormat = "yyyy-MM-dd'T'HH:mm:ss"
  for fj in FOIj:
    let initial_request_at =
      if fj["initial_request_at"].kind == JNull: none(DateTime)
      else: some(fj["initial_request_at"].getStr.parse(isoFormat))
    let last_updated_at =
      if fj["last_updated_at"].kind == JNull: none(DateTime)
      else: some(fj["last_updated_at"].getStr.parse(isoFormat))
    let tags = collect(newSeq):
      for tj in fj["tags"]:
        tj.getStr
    FOIs.add(FOI(
      title: fj["title"].getStr,
      link: fj["link"].getStr,
      status: fj["status"].getStr,
      wdtk_id: fj["wdtk_id"].getStr,
      tags: tags,
      last_updated_at: last_updated_at,
      initial_request_at: initial_request_at
    ))
  res = buildHtml():
      text fmt"Added {FOIs.len} FOIs"

ajaxGet("first_1000.json", @[], loadFOIs)

proc render(): VNode =
  result = buildHtml(tdiv(class="foi-wrapper")):
    section(class="foi-list"):
      h2:
        text "FOIs"
      for f in FOIs:
        h3: a(href=f.link):
          text f.title
        if f.last_updated_at.isSome:
          let ts = f.last_updated_at.get.format("yyyy-MM-dd")
          p:
            text fmt"Last Updated at {ts}"
        if f.initial_request_at.isSome:
          let ts = f.initial_request_at.get.format("yyyy-MM-dd")
          p:
            text fmt"Request submitted on {ts}"
        p:
          for t in f.tags:
            text fmt"{t} "

  
setRenderer render
