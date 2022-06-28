import streamlit as st
import pystac
import eo_snuggs
from osgeo import gdal
import snuggs
from sklearn.preprocessing import Normalizer

#from ..app import data_context

from urllib.parse import urlparse

settings = None

def get_common_name(asset):

    if "eo:bands" in asset.to_dict().keys():
        if "common_name" in asset.to_dict()["eo:bands"][0].keys():
            return asset.to_dict()["eo:bands"][0]["common_name"]

    return None


def get_asset(item, common_name):

    for _, asset in item.get_assets().items():

        if not "data" in asset.to_dict()["roles"]:
            continue

        eo_asset = pystac.extensions.eo.AssetEOExtension(asset)
        if not eo_asset.bands:
            continue
        for b in eo_asset.bands:
            if (
                "common_name" in b.properties.keys()
                and b.properties["common_name"] == common_name
            ):
                return asset

def vsi_href(uri):

    parsed = urlparse(uri)
    if parsed.scheme.startswith("http"):
        return "/vsicurl/{}".format(uri)
    elif parsed.scheme.startswith("file"):
        return uri.replace("file://", "")
    elif parsed.scheme.startswith("s3"):
        if settings:
            for key, value in settings._asdict().items():
                gdal.SetConfigOption(key, value)
        return "/vsis3/{}".format(uri.strip("s3://"))
    else:
        return uri

# Model

class Model(object):
    def __init__(self, items, roi):

        self.roi = roi
        self.items = items

        self.ctx = load_ctx(items=self.items, roi=self.roi)

    title = "S expressions for Earth Observation"

    label = "Expression"

    default_expression = "(* 1 (threshold_otsu (cva (standardization (asarray red1 green1 blue1 nir1)) (standardization (asarray red2 green2 blue2 nir2)))))"

    def process_expression(self, s_expression):

        print(f"Processing s_expression")

        data = eo_snuggs.eval(s_expression, **self.ctx)

        if data.min() >= 0 and data.max() <= 1:
            return (data * 255).astype(int)
        elif data.shape[2] == 3:
            return data
        else:  # x = data.reshape(data.shape[0] * data.shape[1])
            _sc = Normalizer()
            _sc.fit_transform(data)
            return (_sc.transform(data).reshape(data.shape) * 255).astype(int)

    def check_expression(self, expression):

        with snuggs.ctx(**self.ctx):
            try:
                result = snuggs.expr.parseString(expression)
                return (True, f"Expression is valid")
            except snuggs.ParseException:
                return (False, f"Expression is not valid")
            except snuggs.ExpressionError as e:
                return (False, f"Expression syntax error at position {e.offset}")


@st.experimental_singleton
def load_ctx(items, roi):

    print("loading data for s-expressions")

    cbns = ["red", "green", "blue", "nir"]

    ctx = {}
    for index, item_url in enumerate(items):
        print(f"Open {item_url}")

        item = pystac.read_file(item_url)

        for cbn in cbns:
            asset = get_asset(item, cbn)
            
            print(f"read asset {cbn} for context {cbn}{index + 1 }")
            ds = gdal.Open(
                    vsi_href(asset.href))

            band = ds.GetRasterBand(1)
            ctx["{}{}".format(cbn, index + 1)] = band.ReadAsArray(*roi).astype(float)

            ds = None
    return ctx



# View and controller

model = Model(
    items = ["https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/S2B_10TFK_20210713_0_L2A",
             "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a-cogs/items/S2B_10TFK_20210901_0_L2A"
             ], roi=[1000, 1000, 6000, 4500]
)


def app():

    st.title(model.title)

    def check_expression(args):

        outcome, msg = model.check_expression(st.session_state[args])

        if outcome:
            st.success(msg)
        else:
            st.error(msg)

    expression_input = st.text_input(
        key="s_expression",
        label=model.label,
        value=model.default_expression,
        on_change=check_expression,
        args=("s_expression",),
    )

    if st.button(label="Process"):
        with st.spinner("Processing the s_expression..."):

            data = model.process_expression(s_expression=expression_input)

            st.image(data)
            st.success("Done!")
