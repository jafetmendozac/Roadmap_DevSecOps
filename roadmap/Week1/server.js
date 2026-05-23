const net = require('net');

// En Node.js, los servidores TCP se crean con el módulo nativo net. Cuando un cliente (como el navegador) se conecta y envía una petición, el servidor recibe esos datos dentro de un evento llamado 'data', pero no llegan como texto plano, sino en forma de datos binarios conocidos como Buffer 
// node server.js to run the server, then open a browser and navigate to http://localhost:3000/contacto to see the output in the terminal. You should see a warning about the User-Agent being too long, along with the method and path of the request.

let mockResponse = [
  "GET /contacto HTTP/1.1",
  "Host: miservidor.com",
  "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) ajdf;oakkldf'asjfkj'asdkfj'ksdjf'klsjdf",
  "Accept: text/html"
];

function format(lineas, socket) {
    const [method, path] = lineas[0].split(" ");
    const userAgent = lineas.find(l => l.includes("User-Agent"));
    const regex = /User-Agent:\s*.{50,}/;
    
    if (regex.test(userAgent)) {
        console.log("Warning: User-Agent is too long");
        socket.destroy();
    } else {
        console.log(`[${method}] Petición a '${path}' desde ${userAgent}`);
    }
}

const server = net.createServer((socket) => {
    console.log('¡Cliente conectado!');
    
    socket.on('data', (bufferData) => {
        const peticionTexto = bufferData.toString();
        const lineas = peticionTexto.split('\r\n');
        format(lineas, socket);
    });

    socket.on('end', () => {
        console.log('Cliente desconectado.');
    });
});

server.listen(3000, () => {
    console.log('Servidor escuchando en el puerto 3000');
});
