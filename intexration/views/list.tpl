<!doctype html>

<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta name="description" content="InTeXration">
	<meta name="author" content="InTeXration">

	<title>InTeXration</title>

    <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{base_url}}css/style.css">
    <style type="text/css">
    body {
        background-color: #f5f5f5;
        padding-top: 70px;
        height: 100%;
    }

    .item {
        background: #fff;
        border: 1px solid #dae1e8;
        -webkit-border-radius: 4px;
        -moz-border-radius: 4px;
        border-radius: 4px;
    }
    .item .item-header {
        padding: 15px;
        background: #f1f1f1;
        border-bottom: 1px solid #dae1e8;
        -webkit-border-radius: 4px 4px 0 0;
        -moz-border-radius: 4px 4px 0 0;
        border-radius: 4px 4px 0 0;
        color: #dae1e8;
        *zoom: 1;
    }

    .item .item-header:after,
    .item .item-content:after {
        clear: both;
    }
    .item .item-content {
        padding: 15px;
        -webkit-border-radius: 0 0 4px 4px;
        -moz-border-radius: 0 0 4px 4px;
        border-radius: 0 0 4px 4px;
        *zoom: 1;
    }

    .panel tr th {
        width: 60%
    }

    #footer div {
        margin-top: 50px;
        font-size: 10pt;
        text-align: center;
    }

    .document tr th, .document tr td {
        width: 16%;
    }

    </style>
</head>

<body>

	<!-- Fixed navbar -->
	<div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
		<div class="container">
			<div class="navbar-header">
				<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
					<span class="sr-only">Toggle navigation</span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
				</button>
				<a class="navbar-brand" href="#">InTeXration</a>
			</div>
			<div class="navbar-collapse collapse">
				<ul class="nav navbar-nav">
					<li class="active"><a href="#">Overview</a></li>
				</ul>
				<ul class="nav navbar-nav navbar-right">
					<li><a href="https://github.com/JDevlieghere/InTeXration" class="active">GitHub</a></li>
				</ul>
			</div><!--/.nav-collapse -->
		</div>
	</div>

	<div class="container">

		<div class="row">
			<div class="col-md-9">
				% for identifier in documents:
				<div class="document">
					<h3>{{identifier.name}}</h3>
					<table class="table">
					<tr>
						<th>Owner</th>
						<td>{{identifier.owner}}</td>
						<th>Errors</th>
						<td>{{len(documents[identifier].errors())}}</td>
						<th>PDF</th>
						<td><a href="{{base_url}}pdf/{{identifier.owner}}/{{identifier.repository}}/{{identifier.name}}">link</a></td>
					</tr>
					<tr>
						<th>Repository</th>
						<td>{{identifier.repository}}</td>
						<th>Warnings</th>
						<td>{{len(documents[identifier].warnings())}}</td>
						<th>Log</th>
						<td><a href="{{base_url}}log/{{identifier.owner}}/{{identifier.repository}}/{{identifier.name}}">link</a></td>
					</tr>
					</table>
				</div>
				% end
			</div>
			<div class="col-md-3">

				<div class="panel panel-default">
					<div class="panel-heading">Statistics</div>
					<table class="table">
					<tr>
						<th>Documents</th>
						<td>{{len(documents)}}</td>
					</tr>
					<tr>
						<th>Queued</th>
						<td>{{len(queue)}}</td>
					</tr>
					</table>
				</div>

				<div class="panel panel-default">
					<div class="panel-heading">Configuration</div>
					<table class="table">
					<tr>
						<th>Branch</th>
						<td>{{branch}}</td>
					</tr>
					<tr>
						<th>Lazy</th>
						<td>{{lazy}}</td>
					</tr>
					<tr>
						<th>Threaded</th>
						<td>{{threaded}}</td>
					</tr>
					</table>
				</div>

			</div>
		</div>
	</div>

	<div id="footer">
    	<div class="container">
     		<p class="credit">InTeXration - LaTeX Continuous Integration Server</p>
    	</div>
    </div>
	<!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
	<script src="//code.jquery.com/jquery.js"></script>
	<!-- Include all compiled plugins (below), or include individual files as needed -->
	<script src="//netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
</body>
</html>