import express from "express";
import { fileURLToPath } from "url";
import { dirname } from "path";
import path from "path";
import bodyParser from "body-parser";
import axios from "axios";

const app = express();
const port = 3000;

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
app.use(express.static("public"));
app.use(bodyParser.urlencoded({ extended: true }));

app.get("/", (req, res) => {
  res.render("index");
});
////////
app.get("/redirect", (req, res) => { 
  res.redirect("http://localhost:3000");
});

app.get("/vision", (req, res) => {
  res.render("vision");
});

app.get("/team", (req, res) => {
  res.render("team");
});


app.post("/chat", async (req, res) => {
  const userMessage = req.body.message;
  try {
    const response = await axios.post("http://localhost:5000/process", {
      message: userMessage,
    });
    res.send(response.data);
  } catch (error) {
    res.send({ botResponse: "Sorry, something went wrong." });
  }
});

app.listen(port, () => {
  console.log(`Server running on port ${port}.`);
});