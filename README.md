# model-mocker

**model-mocker** is an asynchronous Python tool that automatically generates mock data for [Pydantic](https://docs.pydantic.dev/) models. It uses [Faker](https://faker.readthedocs.io/) under the hood to intelligently fill in fields based on their name and type – making it perfect for testing, prototyping APIs, or populating local databases with realistic fake data.

---

## ✨ Features

- ✅ Generate realistic fake data from your Pydantic model definitions
- 🧠 Field-based string heuristics (`email`, `name`, `phone`, etc.)
- 🔁 Supports nested models and lists
- 💤 Asynchronous API for modern Python projects
- 🧪 Compatible with both Pydantic v1 and v2
- 🔌 Easily extendable with custom generators

---

## 🚀 Installation

### With [PDM](https://pdm.fming.dev):

```bash
pdm add model-mocker
```

### With [pip]
```bash
pip install model-mocker
```