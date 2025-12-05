from flask import Flask
from flask import request
from flask import Response

#from flask import send_file
import io

app = Flask(__name__)

from PIL import Image
import numpy as np

#import gen_images

import makeAmoebasX
import amoeba2Dxx
import amoebaSegments2x
import render #render_amoeba(buf, xs, ys, onval=255, clear_buf=True):

@app.route("/am/")
def create_app():
		#size = request.args.get('size')  # Get 'param1' value, None if not present
		#ng = request.args.get('ng')  # Get 'param1' value, None if not present
		seed=request.args.get('seed')
		#target_present=request.args.get('targ')
		#clutter_present=request.args.get('clut')
		#nontarget_present=request.args.get('nontarg')

		size=256
		ng=12
		target_present=1
		clutter_present=0
		nontarget_present=0
		
		np.random.seed(int(seed))

		buf=gen_images.gen1(int(target_present),int(ng),int(size),int(size),clutter_present=int(clutter_present),nontarget_present=int(nontarget_present) )
		buf=(buf>0)*255
		buf=np.array(255-buf,dtype='uint8')

		img = Image.fromarray(buf, 'L' )

		# Save the image to a bytes buffer
		img_byte_arr = io.BytesIO()
		img.save(img_byte_arr, format='PNG')
		img_byte_arr.seek(0)
	
		resp=Response(img_byte_arr.read(), mimetype='image/png')
		resp.headers.add('Access-Control-Allow-Origin', '*')
		return resp

@app.route("/amx/")
def create_app2():
		seed_target=request.args.get('seed_target')
		seed_clutter=request.args.get('seed_clutter')
		size=request.args.get('size')

		DEBUG_COLORS=False

		is_target = (int(seed_target)>=0)
		amoeba_struct = makeAmoebasX.AmoebaStruct(is_target,size)

		if is_target:
			amoeba_struct.num_targets = 1
		else:
			amoeba_struct.num_targets = 0
		amoeba_struct.num_distractors   = 4 - amoeba_struct.num_targets
		res=amoeba2Dxx.amoeba2Dxx( amoeba_struct, seed_target, seed_clutter )
		[s,xs,ys]=res
		buf = np.zeros((amoeba_struct.image_rect_size, amoeba_struct.image_rect_size), dtype=np.uint8)
		img=render.render_amoeba(buf, xs,ys)
		img = Image.fromarray(255-img, 'L' )

		# Save the image to a bytes buffer
		img_byte_arr = io.BytesIO()
		img.save(img_byte_arr, format='PNG')
		img_byte_arr.seek(0)
	
		resp=Response(img_byte_arr.read(), mimetype='image/png')
		resp.headers.add('Access-Control-Allow-Origin', '*')
		return resp

@app.route('/img')
def img():
		param1 = request.args.get('param1')  # Get 'param1' value, None if not present
		if not param1 is None:
			siz=int(param1)
		else:
			siz=100
		garr = np.random.randint(0,256,size=(siz,siz), dtype=np.uint8 )
		# Create a simple 8-bit grayscale image (e.g., a 100x100 pixel image)
		#img = Image.new('L', (100, 100), color=128) # 'L' mode for 8-bit grayscale
		img = Image.fromarray(garr, 'L' )

		# Save the image to a bytes buffer
		img_byte_arr = io.BytesIO()
		img.save(img_byte_arr, format='PNG')
		img_byte_arr.seek(0)

		return Response(img_byte_arr.read(), mimetype='image/png')

    #return send_file(
        #io.BytesIO(obj.logo.read()),
        #download_name='logo.png',
        #mimetype='image/png'
    #)



if __name__ == "__main__":
	pass
	# Good:
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=8080)
	# Bad:
#def hello_world():
    #return "<p>Hello, World!</p>"
