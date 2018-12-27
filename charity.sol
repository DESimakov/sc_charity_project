pragma solidity ^0.4.24;


contract shop_prototype{
    address owner = msg.sender;
    
    modifier onlyOwner {
        require(msg.sender == owner) ;
        _;
    }

    function transferOwnership(address _newOwner) public onlyOwner {
        if (_newOwner != address(0)) {
            owner = _newOwner;
        }
    }
    
    uint public value;

    mapping(string => string) names;
    mapping(string => uint256) stats;
    mapping(string => string) discr;
    mapping(string => uint256) prices;

    string[] public goods_ids;
    
    constructor () public {
        string memory key = 'id1';

        names[key] = 'good 1';
        stats[key] = 0;
        discr[key] = 'nice thing';
        prices[key] = 10000;
        goods_ids.push(key); 
        
        key = 'id2';
        names[key] = 'good 2';
        stats[key] = 0;
        discr[key] = 'nice thing 2';
        prices[key] = 20000;
        goods_ids.push(key);
        
        key = 'id3';
        names[key] = 'good 3';
        stats[key] = 0;
        discr[key] = 'nice thing 3';
        prices[key] = 1000000;
        goods_ids.push(key);
    }

    function new_good(string memory _key, string _name, string _discr, uint256 _price) public onlyOwner payable{
        owner.transfer(msg.value);
        names[_key] = _name;
        stats[_key] = 0;
        discr[_key] = _discr;
        prices[_key] = _price;
        goods_ids.push(_key);
    }

    function get_good_name(string memory _key) public view returns (string _name){
        _name = names[_key];
    }

    function get_good_stats(string memory _key) public view returns (uint256 _stats){
        _stats = stats[_key];
    }

    function get_good_discr(string memory _key) public view returns (string _discr){
        _discr = discr[_key];
    }
    
    function get_good_prices(string memory _key) public view returns (uint256 _prices){
        _prices = prices[_key];
    }

    function get_contract_balance() public view onlyOwner returns (uint256) {
        return address(this).balance;
    }

    function transfer_money() public onlyOwner payable{
        value += msg.value;
        owner.call.value(address(this).balance).gas(100000);
        value -= msg.value;
    }

    function get_owner() public view returns (address){
        return owner;
    }
    
    function is_owner() public view returns (bool){
        return msg.sender == owner;
    }
    
    function buy(string memory _key) public payable{
        require(stats[_key] == 0);
        require(msg.value >= prices[_key]);
        value += msg.value;
        owner.transfer(address(this).balance);
        stats[_key] = 1;
    }
    
}