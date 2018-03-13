module.exports = [
	{
		test: /\.jsx?$/,
		exclude: /(node_modules|bower_components|public)/,
		loaders: ['react-hot-loader/webpack']
	},
	{
		test: /\.jsx?$/,
		exclude: /(node_modules|bower_components|public)/,
		loader: 'babel-loader',
		query: {
		  presets: ['es2015', 'react'],
		  plugins: ['transform-runtime', 'transform-decorators-legacy', 'transform-class-properties'],
		}
	},
	{
		test: /\.eot(\?v=\d+\.\d+\.\d+)?$/,
		loader: "file-loader"
	},
	{
		test: /\.(woff|woff2)$/,
		loader: "url-loader?prefix=font/"
	},
	{
		test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/,
		loader: "url-loader?mimetype=application/octet-stream"
	},
	{
		test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
		loader: "url-loader?mimetype=image/svg+xml"
	},
	{
		test: /\.gif/,
		loader: "url-loader?mimetype=image/gif"
	},
	{
		test: /\.jpg/,
		loader: "url-loader?mimetype=image/jpg"
	},
	{
		test: /\.png/,
		loader: "url-loader?mimetype=image/png"
	},
	{
		test: /\.woff2?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
		loader: "url-loader"
	},
];
