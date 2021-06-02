/**
 * 
 * @param {*} options is a JSON defining the following data :
 * type - string
 * url - string
 * data - json
 * dataType - string
 * Example : 
 * type: 'POST',
   url : '/cart/add_to_cart/',
   data: {product_id: 102, quantity: 4},
   dataType: 'json'

   A future object is returned
 */
function ajax(options){
    return new Promise(function(resolve, reject){
        $.ajax(options).done(resolve).fail(reject);
    });
}

var Tabs = (function(){
    function Tabs(){
        this.currentTab     = 0;
        this.tabCount       = 0;
        this.tabs           = {};
        this.tab            = {};
        this.tabsCount      = 0;
        
    };

    Tabs.prototype.init = function(){
        this.tabsCount = $(".tabs").length;
        this.tabs = $(".tab-content");
        this.tab = $(".tab");
        this.tabCount = this.tab.length;
        if(this.tabCount == 0){
            return;
        }
        
        $('div.tab-container').each(function(){
            console.log("tab-container init...");
            $(this).find('div.tab-content:eq(0)').nextAll().hide();
        });
        //this.tabs.hide();
        $('div.tab-bar .tab').click(function(){
            var current = $(this);
            console.log("Tab clicked");
            console.log("current data : ", current.data('toggle'));
            
            if(!current.hasClass('active')){
                console.log("Has no class active");
                current.addClass('active').siblings().removeClass('active');
                $(current.data('toggle')).show().siblings('div.tab-content').hide();
            }
        });
    };
    Tabs.prototype.onTabClicked = function(event){
        var tab = parseInt($(event.target).data("index"));
        if(tab != this.currentTab){
            console.log("Tabs Plugin : Tab Clicked");
            this.currentTab = tab;
                this.update();
        }
    };
    Tabs.prototype.update = function(){
        this.tab.removeClass("active");
        $(this.tab[this.currentTab]).addClass("active");
        var that = this;
        this.tabs.hide();
        $(this.tabs[this.currentTab]).show();
    };
    return Tabs;
})();



var Slider = (function(){
    function Slider(){
        images_src = ['customer.png', 'businessman.png'];
    };

    Slider.prototype.init = function(){
       var slider =  $('#slider');
       var slides= slider.find('.slide');
       if(slides.length == 0){
           console.log("No slide found in this page");
           return;
       }

       console.log("slide found in this page : ", slides.length);
       slides.nextAll().hide();
       slides.first().html("I'm Slide 1");
    };

    return Slider;
})();


var UserRechargeAccount = (function(){
    function UserRechargeAccount(){
        this.form = $("voucher-recharge-form");
        if(this.form.length == 0){
            console.log("no voucher recharge form found on this page");
            return;
        }
        this.amount = $("#amount", this.form);
        this.customer = $("#customer", this.form);
    }

    UserRechargeAccount.prototype.init = function(){
        this.re = RegExp('^[0-9]+$');
        regex = this.re;
        var that = this;
        this.form.on('submit', function(event){
            event.preventDefault();
            var flag = false;
            flag = regex.test(that.amount.val());
            if(!flag){
                $('#amount-error').show();
            }
            else{
                $('#amount-error').hide();
            }
            return flag;
        });
    }



    return UserRechargeAccount;
});

var CaseIssue = (function(){
    function CaseIssue(options){
        console.log("Issue construction...");
        this.template = $("#case-form-wrapper.template");
        if(options && options.selector){
            this.form_selector = options.selector;
        }
        else{
            this.form_selector = "#case-form";
        }
        console.log("Issue constructed ...");
        this.init();

    }

    CaseIssue.prototype.init = function(){
        if(this.form_selector){
            this.form = $(this.form_selector);
            if(this.form.length == 0){
                console.log("No Case Issue form found on this page");
                return;
            }
            var form = this.form;
            $(".modal .modal-body").on("submit", "#case-form",function(event){
            event.preventDefault();
            var flag = true;
            
            var $reporter = $("#reporter", this);
            var $participant = $("#participant", this);
            var $reference = $("#reference", this);
            var $description = $("#case-description", this);

            var reporter = $reporter.val();
            var participant = $participant.val();
            var reference = $reference.val();
            var description = $description.val();
            var fields = [participant, reference, description];
            var errors_fields = $("#participant-error , #reference-error , #case-description-error",this);
            
            fields.forEach(function(field, index){
                //console.log("Field #\n",index);
                if(field.length > 0){
                    $(errors_fields[index]).hide();
                }else{
                    //console.log("Field #", index, " is incorrect\n");
                    $(errors_fields[index]).show();
                    flag = false;
                }
            });
            if(flag){
                console.log("Reporter : ", reporter, " - Participant : ", participant, " - Ref : ", reference, " - Description : ", description);
            }
            else{
                console.log("The issue form contains invalid fields");
            }
            return flag;
            });
        }
        else{
            return;
        }

    };

    CaseIssue.prototype.create = function(){
        var issue = null;
        issue = this.template.clone().removeClass("template");
        console.log("new CaseIssue element created");
        return issue;
    };

    return CaseIssue;
})();


var Modal = (function(){
    function Modal(options){
        this.init();
        if(options ){
            this.transaction_factory = options.transaction_factory;
            this.factories = options.factories;
        }
        

    }


    Modal.prototype.init = function(){
        that = this;
        var trigger = $(".open-modal").click(function(event){
            var target = $($(this).data('target'));
            //console.log("opening modal ...");
            var options = {template: $(this).data('template'), modal: $(this).data('target'), factory:$(this).data('factory')};
            that.create(options);
            target.show();
        });

        $("body .modal").on("click", ".close-modal", function(event){
            //console.log("Close modal clicked");
            var target = $($(this).data('target'));
            target.hide();
            $(".modal-content .modal-body", target).empty();

        });
        if(window){
            $(window).click(function(event){
                var target = $(event.target);
                if(target.hasClass("modal")){
                    //console.log("Closing current modal");
                    target.hide();
                    $(".modal-content .modal-body", target).empty();
                }
            });
        }
    }

    Modal.prototype.create = function(options){
        var template = this.factories[options.factory].create();
        var modal = $(options.modal);
        $(".modal-content .modal-body", modal).append(template);
        //console.log("added into the modal");

    }
    return Modal;
})();


var Notify = (function(){
    function Notify(){
        this.template = $("#notify");
    }

    Notify.prototype.init = function(){
        $(".modal .modal-body").on("click", "#notify .close", function(event){
            var target = $($(this).data("target"));
            target.hide();
            $(".modal-body", target).empty();
        });

    };

    Notify.prototype.notify = function(data){
        if(data && data.hasOwnProperty('msg')){
            alert(data.msg);
        }
        else{
            alert("Notify called with wrong parameters");
        }
    };

    Notify.prototype.create = function(){

        var template = null;
        template = this.template.clone().removeClass("template");
        console.log("new Notification template element created");
        return template;
    };

    return Notify;
})();



var Collapsible = (function(){
    function Collapsible(){
        this.$collapsible   = {}; // all element with collapsible class
        this.$close         = {}; // all button used to close a collapsible elements.

    }
    Collapsible.prototype.init = function(){
        console.log("Initializing Collapsible ...");
        this.$collapsible = $(".collapsible");
        //this.$close = this.$collapsible.find(".close");
        
        if(this.$collapsible.length == 0){
            console.log("No collapsible found on this page.");
            return;
        }
        this.$collapsible.children('.collapse-content').hide()
        console.log("Found " + this.$collapsible.length + " collapsibles on this pages.");
        $(this.$collapsible).on("click", ".open", function(event){
            console.log(this);
            var target =$(event.target).data("target");
            //var taret = $(this).siblings(".collapse-content");
            if(target == undefined){
                console.log("collpasible : target undefined");
                $(this).parent().children(".collapse-content").toggle();
            }
            else{
                $(target).toggle();
            }
        });

        $(this.$collapsible).on("click", ".close", function(event){
            event.stopPropagation();
            var target =$(event.target).data("target");

            if(target == undefined){
                $(this).parent().toggle();
            }
            else{
                $(target).toggle();
            }
        });

        console.log("Initializing Collapsible done.");
    };

    return Collapsible;
})();



var TableFilter = (function(){
    function TableFilter (){
        this.tables = {};
        this.rowStep = 5; // default number of row to display per page
        this.currentRowIndex = 0;
        this.numberOfRows = 0;
        this.rows = [];
        this.interval_start = {};
        this.interval_end = {};
        this.element_table_row_number = {};

    }
    TableFilter.prototype.init = function (){
       var that = this;
       this.tables = $(".js-filter-table");
       this.table = $('#employee-list');
       this.tableTbody = $('tbody', this.table);
       this.tr = $('tr', this.tableTbody).hide();
       this.numberOfRows = this.tr.length;
       this.element_table_row_number = $(".js-table-rows-number");
       this.interval_start = $(".js-table-interval-start");
       this.interval_end = $(".js-table-interval-end");
       var n = this.tables.length;
       var $select = $("#table-step");
       
       if(n == 0){
           console.log("No filter table found on this page");
           return;
       }
       Array.prototype.push.apply(this.rows, this.tr.toArray());
       if($select.length > 0){
            this.rowStep = $select.val();
            $select.on('change', function(event){
                that.setStep($select.val());
                console.log("table step changed to %s", that.rowStep );
            });
       }
       
       this.updateTable();
     
       console.log("%s filter table found on this page", n);

    }

    TableFilter.prototype.setStep = function(step){
        if(isNaN(step)){
            console.warn("TableFilter::setStep() : step is undefined");
            return;
        }
        var n = parseInt(step);
        if(n != this.rowStep){
            this.rowStep = n;
            this.updateTable();
        }
        
    }

    TableFilter.prototype.showRows = function(start, last){
        console.log("Table current rows interval :  start  - last  -> [%s - %s]", start, last);
            this.rows.forEach(function(tr, index){
                if(index >= start && index < last){
                    $(tr).show();
                }else{
                    $(tr).hide();
                }
            });
            this.interval_start.html(parseInt(start+1));
            this.interval_end.html(parseInt(last));
            this.element_table_row_number.html(parseInt(this.numberOfRows));
    }

    TableFilter.prototype.previous = function(){
        var start = 0;
        var last = 0;
        var tmp = this.currentRowIndex - this.rowStep;
        if( (this.currentRowIndex != 0) && !(tmp < 0)){
            last = this.currentRowIndex;
            start = tmp;
            this.currentRowIndex = start;
            this.showRows(start, last);
        }
    }
    
    TableFilter.prototype.next = function(){
        var start = 0;
        var last = 0;
        var tmp = this.currentRowIndex + this.rowStep;
        if(tmp < this.numberOfRows){
            start = tmp;
            this.currentRowIndex = start;
        }else{
            return;
        }
        if(start + this.rowStep < this.numberOfRows){
            last = start + this.rowStep;
        }else{
            last = this.numberOfRows;
        }
        this.showRows(start, last);
    }

    TableFilter.prototype.updateTable = function(){
        console.log("Table update entry :  currentIndex  - numberOfRows  -> [%s - %s]", this.currentRowIndex, this.numberOfRows);
        var start = this.currentRowIndex;
        var last = 0;
        var tmp = this.currentRowIndex + this.rowStep;
        if(tmp < this.numberOfRows){
            last = tmp;
        }else{
            last = this.numberOfRows;
        }
        this.showRows(start, last);
    }

    TableFilter.prototype.onAdd = function(event, n){
        if(isNaN(n)){
            console.warn("n is undefined");
            return;
        }
        var last = parseInt(n);
        for(var i = 0; i < last; i++){
            this.addRow({company: "novomind AG", name:"Cyrille Ngassam Nkwenga"});
        }
        this.updateTable();
        
    }
    TableFilter.prototype.addRow = function(data){
        var table = $('#employee-list');
        if(table.length == 0){
            console.log("No Employee List Table found");
            return;
        }
        if(typeof data == "undefined"){
            console.log("Data Table Error : data is undefined");
            return;
        }
        var attrs = ["company", "name"];
        var valid = attrs.every(function(e){
            return data.hasOwnProperty(e);
        });
        if(!valid){
            console.log("TableFilter.addRow : data is invalid");
            return;
        }
        this.numberOfRows++;
        var markup = `<tr><td class="checkbox"><input type="checkbox" name="selected"></td> <td>${data.company} - ${this.numberOfRows}</td> <td>${data.name}</td> </tr>`;
        var tbody = $('tbody', table);
        var $tr = $(markup).hide().appendTo(tbody);
        this.rows.push($tr);
    }

    TableFilter.prototype.fetchData = function(){
        console.log("TableFilter::fetchData () not implemented yet");
    }
    return TableFilter;
})();

var notify = new Notify();


function fetchTransaction(){
    $.ajax({
        url: "transactions",
        type: 'post',
        success : function(data){
            notify.notify({msg: "Nouvell Transaction sur votre compte"});
        },
        error: function(data){
            notify.notify({msg: "Error : Votre compte n'a pas pu etre actualisé"});
        },
        complete: function(data){
            setTimeout(fetchTransaction, 60000);
        }
    });
}


var Group = (function(){
    function Group(){
        this.selected_permissions = {};
        this.group_users = {}
        this.add_selected_permissions_btn = {};
        this.add_selected_users_btn = {};
        this.remove_selected_permissions_btn = {};
        this.remove_selected_users_btn = {};
        
    };

    Group.prototype.init = function(){
        $('#add-selected-users').on('click', function(event){
            event.preventDefault();
            var $target = $($(this).data('target'));
            var $source = $($(this).data('source'));
            $('option:selected', $source).appendTo($target);
            $('option', $target).prop('selected', true).addClass('selected');

        });

        $('#add-selected-permissions').on('click', function(){
            var $target = $($(this).data('target'));
            var $source = $($(this).data('source'));
            $('option:selected', $source).appendTo($target);
            $('option', $target).prop('selected', true);

        });

        $('#remove-selected-users').on('click', function(){
            var $target = $($(this).data('target'));
            var $source = $($(this).data('source'));
            $('option:selected', $source).appendTo($target);
            $('option', $target).prop('selected', true).addClass('selected');

        });

        $('#remove-selected-permissions').on('click', function(){
            var $target = $($(this).data('target'));
            var $source = $($(this).data('source'));
            $('option:selected', $source).appendTo($target);
            $('option', $target).prop('selected', true).addClass('selected');

        });
    };


    return Group;
})();


var PermissionGroupManager = (function(){
    function PermissionGroupManager(){
        this.selected_permissions = {};
        this.group_users = {}
        this.add_selected_permissions_btn = {};
        this.add_selected_users_btn = {};
        this.remove_selected_permissions_btn = {};
        this.remove_selected_users_btn = {};
        
    };

    PermissionGroupManager.prototype.init = function(){
        $('#available-permission-list').on('click','li', function(event){
            event.preventDefault();
            var $target = $('#permission-list');
            var self = $(this);
            var $selected_permissions = $('#selected-permission-list');
            $selected_permissions.append($('<option/>', {'value': self.data('value'), 'selected': true, 'text': self.text()}));
            self.appendTo($target);
        });

        $('#permission-list').on('click','li', function(event){
            event.preventDefault();
            var $target = $('#available-permission-list');
            var self = $(this);
            $('#selected-permission-list option').filter(function(){
                return this.value == self.data('value');
            }).remove();
            self.removeClass('active').appendTo($target);
        });


        $('#available-user-list').on('click','li', function(event){
            event.preventDefault();
            var $target = $('#user-list');
            var self = $(this);
            var $selected_users = $('#selected-user-list');
            $selected_users.append($('<option/>', {'value': self.data('value'), 'selected': true, 'text': self.text()}));
            self.appendTo($target);
        });

        $('#user-list').on('click','li', function(event){
            event.preventDefault();
            var $target = $('#available-user-list');
            var self = $(this);
            $('#selected-user-list option').filter(function(){
                return this.value == self.data('value');
            }).remove();
            self.removeClass('active').appendTo($target);
        });

    };


    return PermissionGroupManager;
})();

var JSFilter = (function(){
    function JSFilter(){
        console.log("creating JSFilter instance");
        this.init();
        console.log("JSFilter instance created");
    };

    JSFilter.prototype.init = function(){
        console.log("JSFilter instance initializing");
        $('.js-jsfilter-input, .js-list-filter').on('keyup', function(event){
            event.stopPropagation();
            var value = this.value.trim();
            var target_container = this.getAttribute('data-target');
            var el = this.getAttribute('data-element');
            $(target_container + " " +  el).filter(function(){
                $(this).toggle(this.innerHTML.includes(value));
            });
        });

        console.log("JSFilter instance initialized");
    };


    return JSFilter;
})();

var isDirty = false;

function can_leave(){
    isDirty = false;
    //window.onbeforeunload = null;
}

function askConfirmation(event){
    var ret = undefined;
    if(isDirty){
        if(event){
            event.preventDefault();
            event.returnValue = "You have unsubmitted data. Leaving this page will lost the data."
        }
        ret =  "You have unsubmitted data. Leaving this page will lost the data.";
    }else{
        delete event['returnValue'];
    }
    
    return ret;
}

function prevent_leaving(){
    isDirty = true;
    //window.onbeforeunload = onbeforeunload;
}

$(document).ready(function(){
    let tabs = new Tabs();
    tabs.init();

    var filter = new TableFilter();
    filter.init();

    var permissionManager = new PermissionGroupManager();

    var group = new Group();
    permissionManager.init();
    group.init();
    //$(window).on('beforeunload', onbeforeunload);
    window.addEventListener('beforeunload', askConfirmation);
    var scheduled_query = false;
    var query_delay = 800;
    var $user_search_result = $('#user-search-result');
    var $user_search_target = $($user_search_result.data('target'));
    var $user_search_target_name = $($user_search_result.data('target-name'));

    var userSearch = function(options){

        var promise = ajax(options).then(function(response){
            //console.log("User Search succeed");
            //console.log(response);
            $user_search_result.empty();
            response.forEach(function(user, index){
                var full_name = user.first_name + " " +  user.last_name;
                $('<li>').data('user-id', user.id).data('user-name', full_name).html(full_name + " [" + user.username + "]").
                on('click', function(event){
                    event.stopPropagation();
                    var user_id = $(this).data('user-id');
                    var user_name = $(this).data('user-name');
                    $user_search_target.val(user_id);
                    //$(".js-user-search").val(user_name);
                    $user_search_target_name.val(user_name);
                    $user_search_result.hide();
                    $user_search_result.empty();
                }).appendTo($user_search_result);
                $user_search_result.show();
            });

        }, function(error){
            console.log("User Search failed");
            console.log(error);
        });
    }

    $('.js-user-search').on('keyup', function(event){
        event.stopPropagation();
        var query = $(this).val();
        query = query.trim()
        if(query.length == 0 ){
            return;
        }
        var options = {
            url:'/api/user-search/',
            type: 'GET',
            data : {'search': query},
            dataType: 'json'
        };
        if(scheduled_query){
            clearTimeout(scheduled_query);
        }
        scheduled_query = setTimeout(userSearch, query_delay, options);
    });

    $('.js-table-update').on('click', function(event){
        console.log("Updating the Table");
    });
    $('.js-table-next').on('click', function(event){
        console.log("Displaying the next %s row of the Table", filter.rowStep);
        filter.next();
        
    });

    $('.js-table-previous').on('click', function(event){
        console.log("Displaying the next %s row of the Table", filter.rowStep);
        filter.previous();
        
    });

    var collapsible = new Collapsible();
    collapsible.init();
    
    

    $('.js-grid-enable').on('click', function(){
        $(this).toggleClass('active');
        $('body, body > header.header').toggleClass('baseline-16');
    });

    $('.js-need-confirmation').on('click', function(event){
        return confirm("This action is irreversible. Do you to want proceed ?");
    });
    $('.js-menu').on('click', function(){
        $('.site-panel').css('left', 0);
        $('.js-menu-close').show();
        $(this).hide();

    });
    $('.js-menu-close').on('click', function(){
        var panel = $('.site-panel');
        var left = '-' + panel.css('width');
        panel.css('left', left );
        $('.js-menu').show();
        $(this).hide();
    });
    /*
    $('form').on('change', function(event){
        prevent_leaving();
    });
    $('form .js-cancel').on('click', can_leave);
    */
    $('.js-user-selector').on('click', 'li', function(){
        let target = $(this);
        $('#members').append($('<option/>', {'value': target.data('id'), 'selected': true, 'text': target.text()}));
        target.appendTo('#selected-members');
    });
    $('#selected-members').on('click', 'li', function(){
        let target = $(this);
        target.appendTo('.js-user-selector');
        $('#members option').filter(function(){
            return this.value == target.data('id');
        }).remove();
        
    });

    $('.mat-list').on('click', '.mat-list-item', function(){
        $(this).toggleClass('active');
    });
});


