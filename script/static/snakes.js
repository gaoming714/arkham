/*
Copyright (c) 2015 by Captain Anonymous (http://codepen.io/anon/pen/MavGrq)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

A Pen created at CodePen.io. You can find this one at http://codepen.io/anon/pen/MavGrq.

a rainbowed-down version of [grayscale triangle snakes](http://codepen.io/MateiGCopot/pen/eNEpdY), couldn't resist making it ;D

Forked from [Matei Copot](http://codepen.io/towc/)'s Pen [rainbow triangle snakes](http://codepen.io/towc/pen/KpvdNY/).
*/


jQuery(function ($) {

	$.fn.createSnake = function (Options, Callback) {
		var It = this;
		var w = $(It)[0].width = $(It).parent().width(),
			h = $(It)[0].height = $(It).parent().height(),
			ctx = $(It)[0].getContext('2d'),

			opts = {

				count: 50,
				variation: .3,
				baseLife: 50,
				addedLife: 20,

				bgR: 30,
				bgG: 30,
				bgB: 70,

				animate: true,

				repaintAlpha: .15,

				fps: 25,

				sizeGain: .5,

				saturation: "80%",
				lightness: "50%",

				fixedColor: true,
				fixedColorHue: 150,

				positionHorizontal: 'center',
				positionVertical: 'center'
			},

			snakes = [],
			tick = (Math.random() * 360) | 0,
			first = true;



		opts = $.extend(true, opts, Options);
		generateCenterPoint();

		function resize() {
			w = $(It)[0].width = $(It).parent().width();
			h = $(It)[0].height = $(It).parent().height();

			generateCenterPoint();

			setTimeout(function () {
				warmupIterations = 10;
				for (i = 0; i <= warmupIterations; i++) {
					update();
					render();
				}
			}, 1);
		}
		$(window).resize(resize);


		function generateCenterPoint() {
			if (opts.positionHorizontal == "left") { opts.cx = 0; }
			if (opts.positionHorizontal == "center") { opts.cx = w / 2; }
			if (opts.positionHorizontal == "right") { opts.cx = w - 1; }
			if (opts.positionVertical == "top") { opts.cy = 0; }
			if (opts.positionVertical == "center") { opts.cy = h / 2; }
			if (opts.positionVertical == "bottom") { opts.cy = h - 1; }
		}

		function init() {
			$(this).css("opacity", 0);
			snakes.length = 0;

			ctx.fillStyle = 'rgb(' + opts.bgR + ',' + opts.bgG + ',' + opts.bgB + ')';
			ctx.fillRect(0, 0, w, h);

			if (first) {
				if (opts.animate) { warmupIterations = 100; } else { warmupIterations = 300; }
				for (i = 0; i <= warmupIterations; i++) {
					update();
					render();
				}
				$(this).css("opacity", 0);
				if (opts.animate) {
					anim();
				}
				first = false;
			}
		}

		function anim() {

			//window.requestAnimationFrame( anim );
			setInterval(function () {
				update();
				render();
			}, 1000 / opts.fps);
		}

		function update() {

			++tick;

			if (snakes.length < opts.count)
				snakes.push(new Snake);

			snakes.map(function (snake) { snake.update(); });
		}
		function render() {

			ctx.fillStyle = 'rgba(' + opts.bgR + ',' + opts.bgG + ',' + opts.bgB + ',' + opts.repaintAlpha + ')'
			ctx.fillRect(0, 0, w, h);

			snakes.map(function (snake) { snake.render(); });
		}

		function Snake() {

			this.reset();
		}
		Snake.prototype.reset = function () {

			this.x1 = opts.cx + Math.random();
			this.x2 = opts.cx + Math.random();
			this.x3 = opts.cx + Math.random();
			this.y1 = opts.cy + Math.random();
			this.y2 = opts.cy + Math.random();
			this.y3 = opts.cy + Math.random();

			this.rad = Math.random() * Math.PI * 2;

			this.direction = Math.random() < .5 ? 1 : -1;
			this.size = 1;
			this.life = opts.baseLife + Math.random() * opts.addedLife;

			if (opts.fixedColor) {
				this.color = 'hsla(hue, saturation, lightness, alp)'.replace('hue', opts.fixedColorHue + (this.rad / Math.PI / 2 * 50)).replace('saturation', opts.saturation).replace('lightness', opts.lightness);
			} else {
				this.color = 'hsla(hue, saturation, lightness, alp)'.replace('hue', tick + (this.rad / Math.PI / 2 * 50)).replace('saturation', opts.saturation).replace('lightness', opts.lightness);
			}
		}

		Snake.prototype.update = function () {

			--this.life;

			this.size += 1 + (Math.random() * opts.sizeGain) / 2;
			this.direction *= -1;
			this.rad += Math.random() * opts.variation * (Math.random() < .5 ? 1 : -1) + Math.PI / 2 * this.direction;

			var x4 = this.x3 + Math.cos(this.rad) * this.size,
				y4 = this.y3 + Math.sin(this.rad) * this.size;

			this.x1 = this.x2; this.y1 = this.y2;
			this.x2 = this.x3; this.y2 = this.y3;
			this.x3 = x4; this.y3 = y4;

			if (this.life <= 0 || this.x1 > w || this.x1 < 0 || this.y1 > h || this.y1 < 0) this.reset();
		}
		Snake.prototype.render = function () {

			ctx.fillStyle = this.color.replace('alp', .25 + Math.random() * .5);
			ctx.beginPath();
			ctx.moveTo(this.x1, this.y1);
			ctx.lineTo(this.x2, this.y2);
			ctx.lineTo(this.x3, this.y3);
			ctx.fill();
		}

		init();
	}
});


$(function () {

	$("#snakes").createSnake({

		count: 150,
		variation: 1.3,
		baseLife: 1500,
		addedLife: 500,

		bgR: 255,
		bgG: 255,
		bgB: 255,

		repaintAlpha: .3,

		fps: 25,

		sizeGain: 1.5,

		saturation: "80%",
		lightness: "70%",
		positionHorizontal: 'right',
		positionVertical: 'top',

		fixedColor: true,
		fixedColorHue: 190

	});

});
