using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace Map.Controllers
{
    public class WorldMapController : Controller
    {
        //
        // GET: /WorldMap/

        public ActionResult LandArea()
        {
            return View();
        }

        public ActionResult LandAreaData()
        {
            return Json(null, JsonRequestBehavior.AllowGet);
        }
    }
}
