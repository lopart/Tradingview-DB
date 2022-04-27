// detects and removes duplicates

db.tradingview.aggregate([
	{
		"$group": {
			_id: { info: "$info"},
			dups: { $addToSet: "$_id"},
			count: { $sum: 1}
		}
	},
	{
		"$match": {
			count: { "$gt": 1}
		}
	}]).forEach(function(doc) {
	doc.dups.shift();
	db.tradingview.remove({
		_id: {$in: doc.dups}
	});
})
