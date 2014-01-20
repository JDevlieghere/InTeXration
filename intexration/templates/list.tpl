<!doctype html>

<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta name="description" content="InTeXration">
	<meta name="author" content="InTeXration">

	<title>InTeXration</title>

	<link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{root}}css/style.css">
</head>

<body>
<div class="container">

	% for document in documents:
	<div class="document">
		<h1>{{document.name}}</h1>
	</div>
	% end


</div>

</body>
</html>