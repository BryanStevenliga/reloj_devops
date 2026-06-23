from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reloj Digital Premium</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Special+Elite&display=swap');

        body {
            background-color: #030303;
            color: #f4ecd8;
            height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
            overflow: hidden;
            perspective: 1000px;
        }

        #particles {
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0; left: 0;
            z-index: 1;
            pointer-events: none;
        }

        .clock-container {
            position: relative;
            z-index: 2;
            transition: transform 0.1s ease-out;
            transform-style: preserve-3d;
        }

        .clock-board {
            background: linear-gradient(135deg, #0f0c0a 0%, #050403 100%);
            padding: 3.5rem 5rem;
            border-radius: 16px;
            box-shadow: 0 40px 80px rgba(0, 0, 0, 0.95), inset 0 0 25px rgba(255, 85, 0, 0.02);
            border: 2px solid #261c14;
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
            cursor: pointer;
        }

        .clock-board:hover {
            border-color: #ff7700;
            box-shadow: 0 50px 100px rgba(255, 85, 0, 0.15), inset 0 0 40px rgba(255, 85, 0, 0.05);
        }

        .time {
            font-family: 'Orbitron', sans-serif;
            font-size: 7.5rem;
            font-weight: 700;
            color: #ff4500;
            letter-spacing: 6px;
            margin: 0;
            line-height: 1;
            transition: all 0.4s ease;
            text-shadow: 0 0 15px rgba(255, 69, 0, 0.5), 0 0 30px rgba(255, 69, 0, 0.3);
        }

        .clock-board:hover .time {
            color: #ff9f1c;
            text-shadow: 0 0 20px rgba(255, 159, 28, 0.9), 0 0 50px rgba(255, 159, 28, 0.6), 0 0 90px rgba(255, 159, 28, 0.3);
            transform: translateZ(40px);
        }

        .date {
            font-family: 'Special Elite', serif;
            font-size: 2.2rem;
            color: #615043;
            margin-top: 25px;
            letter-spacing: 4px;
            border-top: 1px dashed #261c14;
            padding-top: 20px;
            transition: all 0.4s ease;
        }

        .clock-board:hover .date {
            color: #c2946e;
            border-top-style: solid;
            border-top-color: #4a3525;
            transform: translateZ(20px);
        }
    </style>
</head>
<body>

    <canvas id="particles"></canvas>

    <div class="clock-container" id="interactive-clock">
        <div class="clock-board">
            <div class="time" id="clock">00:00:00</div>
            <div class="date" id="date">-- . -- . ----</div>
        </div>
    </div>

    <script>
        function updateClock() {
            const now = new Date();
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const seconds = String(now.getSeconds()).padStart(2, '0');
            
            const day = String(now.getDate()).padStart(2, '0');
            const months = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC'];
            const month = months[now.getMonth()];
            const year = now.getFullYear();

            document.getElementById('clock').textContent = `${hours}:${minutes}:${seconds}`;
            document.getElementById('date').textContent = `${day} . ${month} . ${year}`;
        }
        setInterval(updateClock, 1000);
        updateClock();

        const clockBox = document.getElementById('interactive-clock');
        document.addEventListener('mousemove', (e) => {
            const xAxis = (window.innerWidth / 2 - e.pageX) / 20;
            const yAxis = (window.innerHeight / 2 - e.pageY) / 20;
            clockBox.style.transform = `rotateY(${xAxis}deg) rotateX(${-yAxis}deg)`;
        });

        document.addEventListener('mouseleave', () => {
            clockBox.style.transform = `rotateY(0deg) rotateX(0deg)`;
        });

        const canvas = document.getElementById('particles');
        const ctx = canvas.getContext('2d');
        let particlesArray = [];

        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 2 + 0.3;
                this.speedX = Math.random() * 0.4 - 0.2;
                this.speedY = Math.random() * -0.4 - 0.05;
                this.alpha = Math.random() * 0.4 + 0.1;
            }
            update() {
                this.x += this.speedX;
                this.y += this.speedY;
                if (this.y < 0) {
                    this.y = canvas.height;
                    this.x = Math.random() * canvas.width;
                }
            }
            draw() {
                ctx.save();
                ctx.globalAlpha = this.alpha;
                ctx.fillStyle = '#4a321a';
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
                ctx.restore();
            }
        }

        function init() {
            for (let i = 0; i < 40; i++) {
                particlesArray.push(new Particle());
            }
        }

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let i = 0; i < particlesArray.length; i++) {
                particlesArray[i].update();
                particlesArray[i].draw();
            }
            requestAnimationFrame(animate);
        }

        init();
        animate();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    # Ponemos debug=False para que Docker Swarm mantenga estable el contenedor en Contabo
    app.run(host='0.0.0.0', port=5000, debug=False)